"use client";

import { useState, useMemo } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, AudioWaveform, MessageSquareWarning, Subtitles, Video } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProjectCard, UploadCard } from "@/components/dashboard";
import { projectsApi } from "@/lib/api";
import { useAuthStore } from "@/stores/auth-store";

// Global variable to pass file between pages (since Next.js App Router doesn't support router state)
declare global {
  var __selectedFile: File | null;
}

const quickTools = [
  {
    name: "Remove Silence",
    description: "Automatically cut silent parts",
    icon: AudioWaveform,
    color: "bg-blue-100 text-primary dark:bg-primary/20 dark:text-primary",
  },
  {
    name: "Word Filter",
    description: "Remove filler words",
    icon: MessageSquareWarning,
    color: "bg-purple-100 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400",
  },
  // {
  //   name: "Auto-Subtitles",
  //   description: "Generate captions instantly",
  //   icon: Subtitles,
  //   color: "bg-green-100 text-green-600 dark:bg-green-500/20 dark:text-green-400",
  // },
  // {
  //   name: "AI Shorts",
  //   description: "Create viral clips from long form",
  //   icon: Video,
  //   color: "bg-amber-100 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400",
  // },
];

export default function DashboardPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const queryClient = useQueryClient();
  const { user } = useAuthStore();
  const [isCreating, setIsCreating] = useState(false);

  const { data: projectsData, isLoading } = useQuery({
    queryKey: ["projects"],
    queryFn: () => projectsApi.list({ limit: 20 }),
  });

  // Get search query from URL
  const searchQuery = searchParams.get("search") || "";

  // Filter projects based on search query
  const filteredProjects = useMemo(() => {
    if (!projectsData?.projects || !searchQuery.trim()) {
      return projectsData?.projects || [];
    }
    return projectsData.projects.filter((project) =>
      project.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [projectsData?.projects, searchQuery]);

  const createProjectMutation = useMutation({
    mutationFn: async (file: File) => {
      const project = await projectsApi.create({ name: file.name.replace(/\.[^/.]+$/, "") });
      await projectsApi.uploadMedia(project.id, file);
      return project;
    },
    onSuccess: (project) => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      router.push(`/projects/${project.id}`);
    },
    onSettled: () => {
      setIsCreating(false);
    },
  });

  const handleFileSelect = (file: File) => {
    // Store file in global variable (Next.js App Router doesn't support router state)
    globalThis.__selectedFile = file;
    router.push("/projects/new");
  };

  const handleEditProject = (projectId: string) => {
    router.push(`/projects/${projectId}`);
  };

  const handleDeleteProject = (projectId: string) => {
    queryClient.invalidateQueries({ queryKey: ["projects"] });
  };

  const handleNewProject = () => {
    router.push("/projects/new");
  };

  const firstName = user?.full_name?.split(" ")[0] || "there";

  return (
    <div className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-8 p-6 lg:p-10">
      {/* Welcome Section */}
      <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-3xl font-black tracking-tight text-foreground sm:text-4xl">
            Welcome back, {firstName}
          </h2>
          <p className="mt-2 text-base text-muted-foreground">
            Ready to create secure content today? All your data is encrypted.
          </p>
        </div>
        <Button onClick={handleNewProject} className="group">
          <Plus className="h-5 w-5 mr-2" />
          New Project
        </Button>
      </div>

      {/* Quick AI Tools */}
      <section>
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-bold text-foreground">Quick AI Tools</h3>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {quickTools.map((tool) => (
            <button
              key={tool.name}
              className="group flex flex-col gap-3 rounded-xl border border-border bg-card p-5 text-left shadow-sm transition-all hover:border-primary/50 hover:shadow-md"
            >
              <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${tool.color}`}>
                <tool.icon className="h-5 w-5" />
              </div>
              <div>
                <h4 className="font-bold text-foreground">{tool.name}</h4>
                <p className="text-xs text-muted-foreground">{tool.description}</p>
              </div>
            </button>
          ))}
        </div>
      </section>

      {/* Recent Projects */}
      <section className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h3 className="text-lg font-bold text-foreground">Recent Projects</h3>
            {projectsData && (
              <span className="rounded-full bg-muted px-2 py-0.5 text-xs font-bold text-muted-foreground">
                {searchQuery.trim() ? filteredProjects.length : projectsData.pagination.total}
                {searchQuery.trim() && ` of ${projectsData.pagination.total}`}
              </span>
            )}
          </div>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="aspect-video rounded-xl bg-muted" />
                <div className="mt-4 h-4 w-3/4 rounded bg-muted" />
                <div className="mt-2 h-3 w-1/2 rounded bg-muted" />
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            <UploadCard onFileSelect={handleFileSelect} />
            {filteredProjects.map((project) => (
              <ProjectCard key={project.id} project={project} onEdit={handleEditProject} onDelete={handleDeleteProject} />
            ))}
          </div>
        )}

        {isCreating && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
            <div className="flex flex-col items-center gap-4 rounded-xl bg-card p-8 shadow-2xl border border-border">
              <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent" />
              <p className="text-sm font-medium text-foreground">Creating project...</p>
            </div>
          </div>
        )}
      </section>

      {/* CTA Banner */}
      {/* <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-primary to-emerald-600 p-8 text-white md:p-12">
        <div className="absolute right-0 top-0 h-full w-1/2 opacity-10">
          <svg className="h-full w-full" preserveAspectRatio="none" viewBox="0 0 100 100">
            <path d="M0 100 L100 0 L100 100 Z" fill="white" />
          </svg>
        </div>
        <div className="relative z-10 flex flex-col items-start gap-4 max-w-2xl">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/20 backdrop-blur-sm">
            <span className="material-symbols-outlined text-3xl">lock</span>
          </div>
          <h2 className="text-2xl font-bold md:text-3xl">Privacy First Editing</h2>
          <p className="text-white/80 max-w-lg">
            Your videos are processed in a secure, isolated environment. We never use your content
            to train our models without your explicit permission.
          </p>
          <Button variant="secondary" className="mt-2 bg-white text-primary hover:bg-white/90">
            View Security Report
          </Button>
        </div>
      </div> */}
    </div>
  );
}
