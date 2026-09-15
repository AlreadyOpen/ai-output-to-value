import * as React from "react"
import { Menu } from "@base-ui/react/menu"
import { cn } from "@/lib/utils"

export const DropdownMenu = Menu.Root

export function DropdownMenuTrigger({ className, ...props }: Menu.Trigger.Props) {
  return <Menu.Trigger className={cn(className)} {...props} />
}

export function DropdownMenuContent({ className, children, ...props }: Menu.Popup.Props) {
  return (
    <Menu.Portal>
      <Menu.Positioner sideOffset={6} align="end" className="z-[120]">
        <Menu.Popup
          className={cn(
            "min-w-56 rounded-md border border-border bg-popover p-1 text-popover-foreground shadow-lg outline-none",
            className,
          )}
          {...props}
        >
          {children}
        </Menu.Popup>
      </Menu.Positioner>
    </Menu.Portal>
  )
}

export function DropdownMenuItem({ className, ...props }: Menu.Item.Props) {
  return (
    <Menu.Item
      className={cn(
        "flex cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none data-[highlighted]:bg-accent data-[highlighted]:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
        className,
      )}
      {...props}
    />
  )
}

export function DropdownMenuLink({ className, ...props }: Menu.LinkItem.Props) {
  return (
    <Menu.LinkItem
      className={cn(
        "flex cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm text-inherit no-underline outline-none data-[highlighted]:bg-accent data-[highlighted]:text-accent-foreground",
        className,
      )}
      {...props}
    />
  )
}

export function DropdownMenuSeparator({ className, ...props }: Menu.Separator.Props) {
  return <Menu.Separator className={cn("-mx-1 my-1 h-px bg-border", className)} {...props} />
}
