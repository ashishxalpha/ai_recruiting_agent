import { ReactNode } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { AlertCircle, FileQuestion, ActivitySquare, Ban, Info } from "lucide-react";
import { StandardResponse } from "@/types/dashboard";

interface DashboardWidgetWrapperProps<T> {
  title: string;
  description?: string;
  isLoading: boolean;
  isError: boolean;
  data: StandardResponse<T> | undefined;
  children: (data: T) => ReactNode;
  icon?: ReactNode;
  className?: string;
  contentClassName?: string;
}

export function DashboardWidgetWrapper<T>({ 
  title, 
  description, 
  isLoading, 
  isError, 
  data, 
  children,
  icon = <ActivitySquare className="w-5 h-5 text-muted-foreground" />,
  className = "",
  contentClassName = "h-[400px]"
}: DashboardWidgetWrapperProps<T>) {
  
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
          <p className="text-sm text-red-500/80">Failed to load {title.toLowerCase()} data.</p>
        </CardContent>
      </Card>
    );
  }

  if (!data) return null;

  if (!data.metadata.feature_available) {
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
          <p className="text-sm font-medium text-muted-foreground">Feature Unavailable</p>
          <p className="text-xs text-muted-foreground mt-2 max-w-[250px]">{data.metadata.message || "This capability has not yet been integrated."}</p>
        </CardContent>
      </Card>
    );
  }

  if (!data.metadata.data_available || !data.data) {
    return (
      <Card className={`border-dashed ${className}`}>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-muted-foreground">
            {icon}
            <span>{title}</span>
          </CardTitle>
        </CardHeader>
        <CardContent className={`flex flex-col items-center justify-center text-center ${contentClassName}`}>
          <Info className="w-10 h-10 text-muted-foreground/50 mb-4" />
          <p className="text-sm font-medium text-muted-foreground">No Data Yet</p>
          <p className="text-xs text-muted-foreground mt-2 max-w-[250px]">{data.metadata.message || "Records will appear here once generated."}</p>
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
