import { useState, useEffect } from "react";
import Link from "next/link";
import { MoreVertical, Play, Edit, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { formatRelativeTime, formatDuration } from "@/lib/utils";
import type { ProjectResponse, ProjectStatus } from "@/types/api";
import { Button } from "@/components/ui/button";
import { projectsApi } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";
import { ConfirmDialog } from "@/components/ui/confirm-dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface ProjectCardProps {
  project: ProjectResponse;
  duration?: number;
  onDelete?: (id: string) => void;
  onEdit?: (id: string) => void;
}

const statusConfig: Record<ProjectStatus, { label: string; color: string }> = {
  created: { label: "Draft", color: "bg-muted-foreground" },
  processing: { label: "Processing", color: "bg-yellow-500" },
  completed: { label: "Ready", color: "bg-green-500" },
  failed: { label: "Failed", color: "bg-destructive" },
};

export function ProjectCard({ project, duration, onDelete, onEdit }: ProjectCardProps) {
  const status = statusConfig[project.status];
  const isProcessing = project.status === "processing";
  const [thumbnailUrl, setThumbnailUrl] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const { toast } = useToast();

  // Load thumbnail with authentication
  useEffect(() => {
    if (!project.thumbnail_url) return;

    const load = async () => {
      const url = await projectsApi.loadThumbnail(project.thumbnail_url);
      setThumbnailUrl(url);
    };

    load();
  }, [project.thumbnail_url]);

  // Cleanup object URL on unmount
  useEffect(() => {
    return () => {
      if (thumbnailUrl) {
        URL.revokeObjectURL(thumbnailUrl);
      }
    };
  }, [thumbnailUrl]);

  const handleEdit = () => {
    onEdit?.(project.id);
  };

  const handleDeleteConfirm = async () => {
    try {
      setIsDeleting(true);
      await projectsApi.delete(project.id);
      onDelete?.(project.id);
      toast({
        title: "Project deleted",
        description: `"${project.name}" has been successfully deleted.`,
      });
    } catch (error) {
      console.error("Failed to delete project:", error);
      toast({
        title: "Failed to delete project",
        description: "Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="group flex flex-col overflow-hidden rounded-xl border border-border bg-card shadow-sm transition-all hover:shadow-md">
      {/* Thumbnail */}
      <Link href={`/projects/${project.id}`} className="relative aspect-video w-full overflow-hidden bg-muted">
        {project.thumbnail_url ? (
          <img
            alt={project.name}
            className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
            src={thumbnailUrl || undefined}
          />
        ) : (
          <div className="h-full w-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center">
            <Play className="h-12 w-12 text-primary/40" />
          </div>
        )}

        {/* Duration badge */}
        {duration && (
          <div className="absolute right-2 top-2 rounded-md bg-black/60 px-1.5 py-0.5 text-[10px] font-bold text-white backdrop-blur-sm">
            {formatDuration(duration)}
          </div>
        )}

        {/* Processing overlay */}
        {isProcessing && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-[1px]">
            <div className="flex flex-col items-center gap-2">
              <div className="h-8 w-8 animate-spin rounded-full border-2 border-white border-t-transparent" />
              <span className="text-xs font-bold text-white">AI Processing...</span>
            </div>
          </div>
        )}

        {/* Hover overlay */}
        {!isProcessing && (
          <div className="absolute inset-0 flex items-center justify-center opacity-0 transition-opacity group-hover:opacity-100 bg-black/30 backdrop-blur-[2px]">
            <button className="rounded-full bg-white p-2 text-foreground shadow-lg hover:scale-110 transition-transform">
              <span className="material-symbols-outlined">edit</span>
            </button>
          </div>
        )}
      </Link>

      {/* Content */}
      <div className="flex flex-1 flex-col justify-between p-4">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <h4 className="line-clamp-1 font-bold text-foreground">{project.name}</h4>
            <p className="mt-1 text-xs text-muted-foreground">
              {formatRelativeTime(project.updated_at)}
            </p>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-foreground">
                <MoreVertical className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={handleEdit}>
                <Edit className="mr-2 h-4 w-4" />
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setIsConfirmOpen(true)}
                disabled={isDeleting}
                className="text-destructive focus:text-destructive w-full"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                {isDeleting ? "Deleting..." : "Delete"}
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>

        {/* Status */}
        <div className="mt-4 flex items-center gap-2">
          <span className={cn("flex h-2 w-2 rounded-full", status.color)} />
          <span className="text-xs font-medium text-muted-foreground">{status.label}</span>
        </div>
      </div>

      <ConfirmDialog
        title="Delete Project"
        description={`Are you sure you want to delete "${project.name}"? This action cannot be undone and will permanently delete all associated files.`}
        confirmText="Delete Project"
        cancelText="Cancel"
        variant="destructive"
        open={isConfirmOpen}
        onOpenChange={setIsConfirmOpen}
        onConfirm={handleDeleteConfirm}
      />
    </div>
  );
}
