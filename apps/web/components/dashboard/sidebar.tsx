"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  FolderOpen,
  Sparkles,
  Settings,
  Diamond,
  Scissors,
} from "lucide-react";
import { Button } from "@/components/ui/button";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  // { name: "Projects", href: "/projects", icon: FolderOpen },
  // { name: "AI Tools", href: "/tools", icon: Sparkles },
  { name: "Settings", href: "/settings", icon: Settings },
];

interface SidebarProps {
  storageUsed?: number;
  storageTotal?: number;
}

export function Sidebar({ storageUsed = 2.5, storageTotal = 10 }: SidebarProps) {
  const pathname = usePathname();
  const storagePercent = (storageUsed / storageTotal) * 100;

  return (
    <aside className="hidden w-64 flex-col justify-between border-r border-border bg-background p-4 md:flex">
      <div className="flex flex-col gap-6">
        {/* Logo */}
        <div className="flex items-center gap-3 px-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-primary-foreground">
            <Scissors className="h-6 w-6" />
          </div>
          <h1 className="text-xl font-bold tracking-tight text-foreground">ClipFlow</h1>
        </div>

        {/* Navigation */}
        <nav className="flex flex-col gap-2">
          {navigation.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )}
              >
                <item.icon className="h-5 w-5" />
                <span className="font-medium">{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Sidebar Footer */}
      {/* <div className="flex flex-col gap-4 px-2">
        <div className="flex flex-col gap-2">
          <div className="flex items-center justify-between text-xs font-medium text-muted-foreground">
            <span>Storage</span>
            <span>
              {storageUsed}GB / {storageTotal}GB
            </span>
          </div>
          <div className="h-1.5 mb-8 w-full overflow-hidden rounded-full bg-muted">
            <div
              className="h-full rounded-full bg-primary transition-all"
              style={{ width: `${storagePercent}%` }}
            />
          </div>
        </div>
        <Button variant="secondary" className="w-full">
          <Diamond className="h-4 w-4 mr-2" />
          Upgrade Plan
        </Button>
      </div> */}
    </aside>
  );
}
