// Modularized Collaboration Workspace Page
import { useState, useEffect, useRef, useCallback } from "react";
import { MessageSquare, FileText, CheckCircle, Activity, Users } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import {
  CollabWorkspaceList,
  CollabChatInterface,
  CollabTeamSidebar,
  CollabDocumentPanel,
  CollabTaskPanel,
  CollabActivityPanel,
  Workspace,
  Message,
  DEMO_WORKSPACES,
  DEMO_MESSAGES,
  wsUrl,
} from "@/components/collaboration/panels";

type TabType = "chat" | "documents" | "tasks" | "activity";

export default function CollaborationPage() {
  // State management
  const [selectedWorkspace, setSelectedWorkspace] = useState<Workspace | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>("chat");
  const [messages, setMessages] = useState<Message[]>(DEMO_MESSAGES);
  const [isLoadingWorkspace, setIsLoadingWorkspace] = useState(false);
  const [isCreatingWorkspace, setIsCreatingWorkspace] = useState(false);

  // WebSocket connection
  const wsRef = useRef<WebSocket | null>(null);

  // Initialize WebSocket connection
  useEffect(() => {
    try {
      const ws = new WebSocket(wsUrl());
      wsRef.current = ws;

      ws.onopen = () => {
        console.log("WebSocket connected");
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === "message") {
            setMessages((prev) => [...prev, data.message]);
          }
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };

      ws.onclose = () => {
        console.log("WebSocket disconnected");
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };

      return () => {
        ws.close();
      };
    } catch (error) {
      console.error("Failed to connect to WebSocket:", error);
    }
  }, []);

  // Event handlers
  const handleSendMessage = useCallback(
    (content: string, attachments?: File[]) => {
      if (!selectedWorkspace) return;

      const newMessage: Message = {
        id: `msg-${Date.now()}`,
        workspaceId: selectedWorkspace.id,
        userId: "1", // Current user ID
        userName: "Dr. Sarah Chen", // Current user name
        content,
        type: "text",
        timestamp: new Date(),
        attachments: attachments
          ? attachments.map((file) => ({
              id: `att-${Date.now()}-${file.name}`,
              name: file.name,
              type: file.type,
              size: file.size,
              url: URL.createObjectURL(file),
            }))
          : [],
      };

      // Add message locally
      setMessages((prev) => [...prev, newMessage]);

      // Send via WebSocket
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(
          JSON.stringify({
            type: "message",
            workspaceId: selectedWorkspace.id,
            message: newMessage,
          }),
        );
      }
    },
    [selectedWorkspace],
  );

  const handleWorkspaceSelect = async (workspace: Workspace) => {
    setIsLoadingWorkspace(true);
    try {
      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 500));
      setSelectedWorkspace(workspace);
      // Filter messages for selected workspace
      const workspaceMessages = DEMO_MESSAGES.filter((m) => m.workspaceId === workspace.id);
      setMessages(workspaceMessages);
    } catch (error) {
      console.error("Error loading workspace:", error);
    } finally {
      setIsLoadingWorkspace(false);
    }
  };

  const handleCreateWorkspace = async () => {
    setIsCreatingWorkspace(true);
    try {
      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 1000));
      console.log("Create new workspace");
      // In real implementation, this would create a workspace and refresh the list
    } catch (error) {
      console.error("Error creating workspace:", error);
    } finally {
      setIsCreatingWorkspace(false);
    }
  };

  const handleMessageAction = (message: Message, action: string) => {
    console.log("Message action:", action, message);
    // Handle message actions like reactions, replies, etc.
  };

  const handleDocumentAction = (document: any, action: string) => {
    console.log("Document action:", action, document);
    // Handle document actions like download, share, etc.
  };

  const handleTaskAction = (task: any, action: string) => {
    console.log("Task action:", action, task);
    // Handle task actions like status change, assignment, etc.
  };

  const handleMemberAction = (member: any, action: string) => {
    console.log("Member action:", action, member);
    // Handle member actions like view profile, change role, etc.
  };

  const workspaceMessages = messages.filter((m) => m.workspaceId === selectedWorkspace?.id);

  return (
    <DashboardLayout
      title="Collaboration"
      subtitle="Real-time workspace collaboration and communication"
    >
      <div className="flex h-[calc(100vh-12rem)] max-w-7xl mx-auto gap-6">
        {/* Left Sidebar - Workspaces */}
        <div className="w-80 flex-shrink-0">
          <Panel className="h-full">
            <CollabWorkspaceList
              workspaces={DEMO_WORKSPACES}
              selectedWorkspace={selectedWorkspace}
              onWorkspaceSelect={handleWorkspaceSelect}
              onCreateWorkspace={handleCreateWorkspace}
              isCreating={isCreatingWorkspace}
            />
          </Panel>
        </div>

        {/* Main Content */}
        <div className="flex-1 min-w-0">
          {selectedWorkspace ? (
            <Panel className="h-full">
              <Tabs
                value={activeTab}
                onValueChange={setActiveTab as any}
                className="h-full flex flex-col"
              >
                <div className="flex-shrink-0 border-b border-gray-200 dark:border-gray-700 px-4 pt-4">
                  <TabsList className="bg-gray-50 dark:bg-gray-800 p-1 rounded-lg">
                    <TabsTrigger value="chat" className="inline-flex items-center gap-2">
                      <MessageSquare size={16} />
                      Chat
                    </TabsTrigger>
                    <TabsTrigger value="documents" className="inline-flex items-center gap-2">
                      <FileText size={16} />
                      Documents
                    </TabsTrigger>
                    <TabsTrigger value="tasks" className="inline-flex items-center gap-2">
                      <CheckCircle size={16} />
                      Tasks
                    </TabsTrigger>
                    <TabsTrigger value="activity" className="inline-flex items-center gap-2">
                      <Activity size={16} />
                      Activity
                    </TabsTrigger>
                  </TabsList>
                </div>

                <div className="flex-1 min-h-0">
                  <TabsContent value="chat" className="h-full m-0 p-0">
                    <CollabChatInterface
                      workspace={selectedWorkspace}
                      messages={workspaceMessages}
                      onSendMessage={handleSendMessage}
                      onMessageAction={handleMessageAction}
                    />
                  </TabsContent>

                  <TabsContent value="documents" className="h-full m-0 p-0">
                    <CollabDocumentPanel
                      workspace={selectedWorkspace}
                      onDocumentAction={handleDocumentAction}
                    />
                  </TabsContent>

                  <TabsContent value="tasks" className="h-full m-0 p-0">
                    <CollabTaskPanel
                      workspace={selectedWorkspace}
                      onTaskAction={handleTaskAction}
                    />
                  </TabsContent>

                  <TabsContent value="activity" className="h-full m-0 p-0">
                    <CollabActivityPanel workspace={selectedWorkspace} />
                  </TabsContent>
                </div>
              </Tabs>
            </Panel>
          ) : (
            <Panel className="h-full flex items-center justify-center">
              {isLoadingWorkspace ? (
                <div className="text-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
                  <p className="text-gray-500 dark:text-gray-400">Loading workspace...</p>
                </div>
              ) : (
                <div className="text-center">
                  <Users size={48} className="mx-auto text-gray-400 mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    Select a Workspace
                  </h3>
                  <p className="text-gray-500 dark:text-gray-400">
                    Choose a workspace from the sidebar to start collaborating.
                  </p>
                </div>
              )}
            </Panel>
          )}
        </div>

        {/* Right Sidebar - Team Members */}
        <div className="w-72 flex-shrink-0">
          <Panel className="h-full">
            {selectedWorkspace ? (
              <CollabTeamSidebar
                workspace={selectedWorkspace}
                onMemberAction={handleMemberAction}
              />
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <Users size={32} className="mx-auto text-gray-400 mb-2" />
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Team members will appear here
                  </p>
                </div>
              </div>
            )}
          </Panel>
        </div>
      </div>
    </DashboardLayout>
  );
}
