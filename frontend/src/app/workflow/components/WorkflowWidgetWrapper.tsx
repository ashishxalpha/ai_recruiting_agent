import { ReactNode } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { AlertCircle, FileQuestion, ActivitySquare, Ban } from "lucide-react";
import { WorkflowResponse } from "@/types/workflow";

interface WorkflowWidgetWrapperProps<T> {
  title: string;
  description?: string;
  isLoading: boolean;
  isError: boolean;
  data: WorkflowResponse<T> | undefined;
  children: (data: T) => ReactNode;
  icon?: ReactNode;
  className?: string;
  contentClassName?: string;
}

export function WorkflowWidgetWrapper<T>({ 
  title, 
  description, 
  isLoading, 
  isError, 
  data, 
  children,
  icon = <ActivitySquare className="w-5 h-5 text-muted-foreground" />,
  className = "",
  contentClassName = "h-[400px]"
}: WorkflowWidgetWrapperProps<T>) {
  
  if (isLoading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            {icon}
            <span>{title}</span>
          </CardTitle>
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
        <CardContent className={`flex items-center justify-center ${contentClassName}`}>
          <div className="space-y-4 w-full h-full flex flex-col justify-center">
            <Skeleton className="h-4/5 w-full" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (isError) {
    return (
      <Card className={`border-red-500/50 ${className}`}>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-red-500">
            <AlertCircle className="w-5 h-5" />
            <span>{title}</span>
          </CardTitle>
        </CardHeader>
        <CardContent className={`flex items-center justify-center ${contentClassName}`}>
          <p className="text-sm text-red-500/80">Failed to load workflow data.</p>
        </CardContent>
      </Card>
    );
  }

  if (!data) return null;

  if (data.status === "no_execution_history") {
    return (
      <Card className={`border-dashed ${className}`}>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-muted-foreground">
            {icon}
            <span>{title}</span>
          </CardTitle>
        </CardHeader>
        <CardContent className={`flex flex-col items-center justify-center text-center ${contentClassName}`}>
          <Ban className="w-10 h-10 text-muted-foreground/50 mb-4" />
          <p className="text-sm font-medium text-muted-foreground">No Execution History</p>
          <p className="text-xs text-muted-foreground mt-2 max-w-[250px]">{data.reason || "This workflow has not executed yet."}</p>
        </CardContent>
      </Card>
    );
  }

  if (data.status === "not_available") {
    return (
      <Card className={`border-dashed ${className}`}>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-muted-foreground">
            {icon}
            <span>{title}</span>
          </CardTitle>
        </CardHeader>
        <CardContent className={`flex flex-col items-center justify-center text-center ${contentClassName}`}>
          <FileQuestion className="w-10 h-10 text-muted-foreground/50 mb-4" />
          <p className="text-sm font-medium text-muted-foreground">Persistence Not Available</p>
          <p className="text-xs text-muted-foreground mt-2 max-w-[250px]">{data.reason || "This module is not currently available."}</p>
        </CardContent>
      </Card>
    );
  }

  if (!data.data) {
     return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            {icon}
            <span>{title}</span>
          </CardTitle>
        </CardHeader>
        <CardContent className={`flex flex-col items-center justify-center text-center ${contentClassName}`}>
          <p className="text-sm font-medium text-muted-foreground">No Data Available</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          {icon}
          <span>{title}</span>
        </CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent className={contentClassName}>
        {children(data.data)}
      </CardContent>
    </Card>
  );
}
