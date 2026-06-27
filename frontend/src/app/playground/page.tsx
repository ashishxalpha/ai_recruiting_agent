"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, FileText, Code, BarChart, Server, Activity } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";

export default function PlaygroundPage() {
  const [file, setFile] = useState<File | null>(null);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">AI Playground</h1>
        <p className="text-muted-foreground mt-2">
          Debug raw extraction, embeddings, and prompt versions.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Input Context</CardTitle>
            <CardDescription>Upload a raw resume.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center text-center">
              <Upload className="w-8 h-8 text-muted-foreground mb-4" />
              <p className="text-sm text-muted-foreground mb-2">Drag and drop resume here</p>
              <Button variant="outline" size="sm">Select File</Button>
            </div>
            
            <div className="space-y-2">
              <h3 className="text-sm font-medium">Configuration</h3>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Prompt Version</span>
                <Badge variant="outline">v1.2.0</Badge>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Embedding Model</span>
                <Badge variant="outline">text-embedding-3-small</Badge>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Extraction Model</span>
                <Badge variant="outline">gpt-4o</Badge>
              </div>
            </div>

            <Button className="w-full">Run AI Pipeline</Button>
          </CardContent>
        </Card>

        <Card className="col-span-2">
          <CardHeader>
            <CardTitle className="flex justify-between items-center">
              <span>Pipeline Output</span>
              <div className="flex space-x-2 text-xs font-normal">
                <Badge variant="secondary" className="flex items-center"><Server className="w-3 h-3 mr-1"/> 4,120 Tokens</Badge>
                <Badge variant="secondary" className="flex items-center"><Activity className="w-3 h-3 mr-1"/> 4.2s Latency</Badge>
              </div>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="raw">
              <TabsList className="mb-4">
                <TabsTrigger value="raw"><FileText className="w-4 h-4 mr-2"/> Raw PDF Text</TabsTrigger>
                <TabsTrigger value="normalized"><Code className="w-4 h-4 mr-2"/> Normalized</TabsTrigger>
                <TabsTrigger value="evaluation"><BarChart className="w-4 h-4 mr-2"/> Evaluation</TabsTrigger>
                <TabsTrigger value="embeddings"><Server className="w-4 h-4 mr-2"/> Embeddings</TabsTrigger>
              </TabsList>
              <TabsContent value="raw">
                <pre className="bg-muted p-4 rounded-md h-[400px] overflow-y-auto text-sm font-mono text-muted-foreground">
                  Waiting for document...
                </pre>
              </TabsContent>
              <TabsContent value="normalized">
                <pre className="bg-muted p-4 rounded-md h-[400px] overflow-y-auto text-sm font-mono text-muted-foreground">
                  Waiting for extraction...
                </pre>
              </TabsContent>
              <TabsContent value="evaluation">
                <div className="h-[400px] flex items-center justify-center border rounded-md text-muted-foreground">
                  No evaluation available
                </div>
              </TabsContent>
              <TabsContent value="embeddings">
                <div className="h-[400px] flex items-center justify-center border rounded-md text-muted-foreground">
                  No vectors generated
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
