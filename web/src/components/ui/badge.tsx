import * as React from "react"
import { cn } from "@/lib/utils"

type BadgeProps = React.HTMLAttributes<HTMLSpanElement> & {
  variant?: "default" | "outline"
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold",
        variant === "default" && "border-border bg-secondary text-secondary-foreground",
        variant === "outline" && "border-border bg-transparent text-foreground",
        className,
      )}
      {...props}
    />
  )
}
