import { ReactNode } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { AlertCircle, FileQuestion, LayoutDashboard } from "lucide-react";
import { AnalyticsResponse } from "@/types/analytics";

interface AnalyticsWidgetWrapperProps<T> {
  title: string;
  description?: string;
  isLoading: boolean;
  isError: boolean;
  data: AnalyticsResponse<T> | undefined;
  children: (data: T) => ReactNode;
  icon?: ReactNode;
}

export function AnalyticsWidgetWrapper<T>({ 
  title, 
  description, 
  isLoading, 
  isError, 
  data, 
  children,
  icon = <LayoutDashboard className="w-5 h-5 text-muted-foreground" />
}: AnalyticsWidgetWrapperProps<T>) {
  
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            {icon}
            <span>{title}</span>
          </CardTitle>
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
        <CardContent className="h-[300px] flex items-center justify-center">
          <div className="space-y-4 w-full h-full flex flex-col justify-end">
            <Skeleton className="h-4/5 w-full" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (isError) {
    return (
      <Card className="border-red-500/50">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-red-500">
            <AlertCircle className="w-5 h-5" />
            <span>{title}</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="h-[300px] flex items-center justify-center">
          <p className="text-sm text-red-500/80">Failed to load analytics data.</p>
        </CardContent>
      </Card>
    );
  }

  if (!data) return null;

  if (data.status === "not_available") {
    return (
      <Card className="border-dashed">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-muted-foreground">
            {icon}
            <span>{title}</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="h-[300px] flex flex-col items-center justify-center text-center">
          <FileQuestion className="w-10 h-10 text-muted-foreground/50 mb-4" />
          <p className="text-sm font-medium text-muted-foreground">Not Yet Implemented</p>
          <p className="text-xs text-muted-foreground mt-2 max-w-[250px]">{data.reason || "This module is not currently available."}</p>
        </CardContent>
      </Card>
    );
  }

  if (!data.data) {
     return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            {icon}
            <span>{title}</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="h-[300px] flex flex-col items-center justify-center text-center">
          <p className="text-sm font-medium text-muted-foreground">No Data Available</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          {icon}
          <span>{title}</span>
        </CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent className="h-[300px]">
        {children(data.data)}
      </CardContent>
    </Card>
  );
}
