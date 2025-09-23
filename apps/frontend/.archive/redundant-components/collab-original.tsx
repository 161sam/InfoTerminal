import React, { useEffect, useMemo, useRef, useState, useCallback } from 'react';
import { 
  Users, 
  MessageSquare, 
  FileText, 
  Plus, 
  Search, 
  Filter, 
  Settings,
  Send,
  Paperclip,
  Smile,
  MoreVertical,
  Pin,
  Download,
  Share2,
  Eye,
  Clock,
  CheckCircle,
  AlertCircle,
  User,
  Hash,
  Folder,
  Star,
  Activity,
  Bell,
  Zap,
  RefreshCw,
  Circle,
  ArrowRight,
  Calendar,
  Tag,
  MessageCircle,
  FolderOpen
} from 'lucide-react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import Panel from '@/components/layout/Panel';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { LoadingSpinner } from '@/components/ui/loading';
import Button from '@/components/ui/button';

interface Workspace {
  id: string;
  name: string;
  description: string;
  members: WorkspaceMember[];
  isPrivate: boolean;
  createdAt: Date;
  updatedAt: Date;
  pinnedItems: string[];
  color: string;
  documentsCount: number;
  tasksCount: number;
  messagesCount: number;
}

interface WorkspaceMember {
  id: string;
  name: string;
  email: string;
  role: 'owner' | 'admin' | 'member' | 'viewer';
  status: 'online' | 'away' | 'offline';
  avatar?: string;
  lastActive: Date;
}

interface Message {
  id: string;
  workspaceId: string;
  userId: string;
  userName: string;
  userAvatar?: string;
  content: string;
  type: 'text' | 'file' | 'task' | 'system';
  timestamp: Date;
  edited?: boolean;
  editedAt?: Date;
  attachments?: Attachment[];
  mentions?: string[];
  reactions?: Reaction[];
  threadId?: string;
  isThread?: boolean;
}

interface Attachment {
  id: string;
  name: string;
  type: string;
  size: number;
  url: string;
  thumbnailUrl?: string;
}

interface Reaction {
  emoji: string;
  users: string[];
  count: number;
}

interface Task {
  id: string;
  workspaceId: string;
  title: string;
  description?: string;
  status: 'todo' | 'in_progress' | 'review' | 'done';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  assignee?: WorkspaceMember;
  reporter: WorkspaceMember;
  dueDate?: Date;
  tags: string[];
  attachments: Attachment[];
  comments: Comment[];
  createdAt: Date;
  updatedAt: Date;
}

interface Comment {
  id: string;
  userId: string;
  userName: string;
  content: string;
  timestamp: Date;
}

interface Document {
  id: string;
  workspaceId: string;
  name: string;
  type: string;
  size: number;
  url: string;
  uploadedBy: WorkspaceMember;
  uploadedAt: Date;
  tags: string[];
  isShared: boolean;
  comments: Comment[];
}

// Demo data
const DEMO_WORKSPACES: Workspace[] = [
  {
    id: '1',
    name: 'Operation Phoenix',
    description: 'High-priority intelligence investigation',
    members: [
      {
        id: '1',
        name: 'Dr. Sarah Chen',
        email: 'sarah.chen@infoterminal.io',
        role: 'owner',
        status: 'online',
        lastActive: new Date()
      },
      {
        id: '2', 
        name: 'Marcus Rodriguez',
        email: 'marcus.r@infoterminal.io',
        role: 'admin',
        status: 'online',
        lastActive: new Date(Date.now() - 300000)
      },
      {
        id: '3',
        name: 'Alex Thompson',
        email: 'alex.thompson@infoterminal.io',
        role: 'member',
        status: 'away',
        lastActive: new Date(Date.now() - 900000)
      }
    ],
    isPrivate: true,
    createdAt: new Date('2024-03-01T10:00:00Z'),
    updatedAt: new Date('2024-03-15T16:30:00Z'),
    pinnedItems: ['msg-1', 'task-1'],
    color: 'red',
    documentsCount: 12,
    tasksCount: 8,
    messagesCount: 245
  },
  {
    id: '2',
    name: 'Market Analysis Q1',
    description: 'Quarterly financial intelligence analysis',
    members: [
      {
        id: '1',
        name: 'Dr. Sarah Chen',
        email: 'sarah.chen@infoterminal.io', 
        role: 'member',
        status: 'online',
        lastActive: new Date()
      },
      {
        id: '4',
        name: 'Emma Wilson',
        email: 'emma.wilson@infoterminal.io',
        role: 'owner',
        status: 'offline',
        lastActive: new Date(Date.now() - 3600000)
      }
    ],
    isPrivate: false,
    createdAt: new Date('2024-02-15T09:00:00Z'),
    updatedAt: new Date('2024-03-14T11:20:00Z'),
    pinnedItems: [],
    color: 'blue',
    documentsCount: 6,
    tasksCount: 4,
    messagesCount: 89
  }
];

const DEMO_MESSAGES: Message[] = [
  {
    id: 'msg-1',
    workspaceId: '1',
    userId: '1',
    userName: 'Dr. Sarah Chen',
    content: 'I\'ve uploaded the preliminary analysis. The patterns we\'re seeing suggest a coordinated effort across multiple vectors.',
    type: 'text',
    timestamp: new Date('2024-03-15T15:30:00Z'),
    attachments: [
      {
        id: 'att-1',
        name: 'preliminary-analysis.pdf',
        type: 'application/pdf',
        size: 2400000,
        url: '/files/preliminary-analysis.pdf'
      }
    ],
    reactions: [
      { emoji: '👍', users: ['2', '3'], count: 2 },
      { emoji: '🔥', users: ['2'], count: 1 }
    ]
  },
  {
    id: 'msg-2',
    workspaceId: '1', 
    userId: '2',
    userName: 'Marcus Rodriguez',
    content: 'Agreed. I\'ve cross-referenced this with our threat intelligence feeds. Creating a task to investigate further.',
    type: 'text',
    timestamp: new Date('2024-03-15T15:45:00Z'),
    mentions: ['1']
  },
  {
    id: 'msg-3',
    workspaceId: '1',
    userId: '3',
    userName: 'Alex Thompson', 
    content: 'The geospatial data from this morning supports that theory. I\'ll run additional correlation analysis.',
    type: 'text',
    timestamp: new Date('2024-03-15T16:00:00Z')
  }
];

function wsUrl() {
  const port = process.env.NEXT_PUBLIC_COLLAB_PORT || process.env.IT_PORT_COLLAB || '8625';
  return `ws://localhost:${port}/ws`;
}

const WORKSPACE_COLORS = {
  red: 'bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-300 dark:border-red-900/30',
  blue: 'bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-900/30',
  green: 'bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-300 dark:border-green-900/30',
  purple: 'bg-purple-100 text-purple-800 border-purple-200 dark:bg-purple-900/30 dark:text-purple-300 dark:border-purple-900/30',
  orange: 'bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/30 dark:text-orange-300 dark:border-orange-900/30'
};

const STATUS_COLORS = {
  online: 'bg-green-500',
  away: 'bg-yellow-500', 
  offline: 'bg-gray-400'
};

// Workspace List Component
function WorkspaceList({ 
  workspaces, 
  selectedWorkspace, 
  onWorkspaceSelect, 
  onCreateWorkspace 
}: {
  workspaces: Workspace[];
  selectedWorkspace?: Workspace;
  onWorkspaceSelect: (workspace: Workspace) => void;
  onCreateWorkspace: () => void;
}) {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredWorkspaces = workspaces.filter(ws =>
    ws.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    ws.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Workspaces</h3>
        <button
          onClick={onCreateWorkspace}
          className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700"
        >
          <Plus size={16} />
          New
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
        <input
          type="text"
          placeholder="Search workspaces..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
        />
      </div>

      {/* Workspace List */}
      <div className="space-y-2">
        {filteredWorkspaces.map((workspace) => (
          <button
            key={workspace.id}
            onClick={() => onWorkspaceSelect(workspace)}
            className={`w-full text-left p-3 rounded-lg border transition-colors ${
              selectedWorkspace?.id === workspace.id
                ? 'bg-primary-50 border-primary-200 dark:bg-primary-900/30 dark:border-primary-900/30'
                : 'bg-white border-gray-200 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className={`w-3 h-3 rounded-full mt-2 ${WORKSPACE_COLORS[workspace.color as keyof typeof WORKSPACE_COLORS].split(' ')[0]}`} />
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-medium text-gray-900 dark:text-white truncate">
                    {workspace.name}
                  </h4>
                  {workspace.isPrivate && (
                    <div className="w-4 h-4 text-gray-400">
                      <Eye size={12} />
                    </div>
                  )}
                </div>
                
                <p className="text-xs text-gray-500 dark:text-gray-400 mb-2 line-clamp-2">
                  {workspace.description}
                </p>
                
                <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
                  <div className="flex items-center gap-1">
                    <Users size={12} />
                    {workspace.members.length}
                  </div>
                  <div className="flex items-center gap-1">
                    <MessageSquare size={12} />
                    {workspace.messagesCount}
                  </div>
                  <div className="flex items-center gap-1">
                    <FileText size={12} />
                    {workspace.documentsCount}
                  </div>
                </div>

                {/* Active members preview */}
                <div className="flex items-center gap-1 mt-2">
                  {workspace.members
                    .filter(m => m.status === 'online')
                    .slice(0, 3)
                    .map((member) => (
                      <div key={member.id} className="relative">
                        <div className="w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                          {member.avatar ? (
                            <img 
                              src={member.avatar} 
                              alt={member.name}
                              className="w-6 h-6 rounded-full object-cover"
                            />
                          ) : (
                            <User size={12} className="text-primary-600 dark:text-primary-400" />
                          )}
                        </div>
                        <div className={`absolute -bottom-0.5 -right-0.5 w-2 h-2 rounded-full border border-white dark:border-gray-800 ${STATUS_COLORS[member.status]}`} />
                      </div>
                    ))}
                  {workspace.members.filter(m => m.status === 'online').length > 3 && (
                    <div className="text-xs text-gray-400 ml-1">
                      +{workspace.members.filter(m => m.status === 'online').length - 3}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

// Chat Interface Component
function ChatInterface({ 
  workspace, 
  messages, 
  onSendMessage 
}: {
  workspace: Workspace;
  messages: Message[];
  onSendMessage: (content: string, attachments?: File[]) => void;
}) {
  const [newMessage, setNewMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    onSendMessage(newMessage);
    setNewMessage('');
  };

  const formatTimestamp = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return date.toLocaleDateString();
  };

  return (
    <div className="flex flex-col h-full">
      {/* Chat Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3">
          <div className={`w-4 h-4 rounded-full ${WORKSPACE_COLORS[workspace.color as keyof typeof WORKSPACE_COLORS].split(' ')[0]}`} />
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">{workspace.name}</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {workspace.members.filter(m => m.status === 'online').length} online
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
            <Search size={16} />
          </button>
          <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
            <MoreVertical size={16} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => {
          const isConsecutive = index > 0 && 
            messages[index - 1].userId === message.userId &&
            (message.timestamp.getTime() - messages[index - 1].timestamp.getTime()) < 300000;

          return (
            <div key={message.id} className={`group ${isConsecutive ? 'ml-12' : ''}`}>
              <div className="flex items-start gap-3">
                {!isConsecutive && (
                  <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
                    {message.userAvatar ? (
                      <img 
                        src={message.userAvatar} 
                        alt={message.userName}
                        className="w-8 h-8 rounded-full object-cover"
                      />
                    ) : (
                      <User size={16} className="text-primary-600 dark:text-primary-400" />
                    )}
                  </div>
                )}
                
                <div className="flex-1 min-w-0">
                  {!isConsecutive && (
                    <div className="flex items-baseline gap-2 mb-1">
                      <span className="font-medium text-gray-900 dark:text-white text-sm">
                        {message.userName}
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {formatTimestamp(message.timestamp)}
                      </span>
                    </div>
                  )}
                  
                  <div className="text-sm text-gray-900 dark:text-gray-100 leading-relaxed">
                    {message.content}
                  </div>

                  {/* Attachments */}
                  {message.attachments && message.attachments.length > 0 && (
                    <div className="mt-2 space-y-2">
                      {message.attachments.map((attachment) => (
                        <div key={attachment.id} className="flex items-center gap-2 p-2 bg-gray-50 dark:bg-gray-800 rounded-lg">
                          <Paperclip size={14} className="text-gray-400" />
                          <span className="text-sm text-gray-700 dark:text-gray-300 flex-1 truncate">
                            {attachment.name}
                          </span>
                          <span className="text-xs text-gray-500">
                            {(attachment.size / 1024 / 1024).toFixed(1)}MB
                          </span>
                          <button className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                            <Download size={14} />
                          </button>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Reactions */}
                  {message.reactions && message.reactions.length > 0 && (
                    <div className="flex items-center gap-2 mt-2">
                      {message.reactions.map((reaction, idx) => (
                        <button
                          key={idx}
                          className="inline-flex items-center gap-1 px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600"
                        >
                          <span>{reaction.emoji}</span>
                          <span className="text-gray-600 dark:text-gray-400">{reaction.count}</span>
                        </button>
                      ))}
                      <button className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity">
                        <Smile size={14} />
                      </button>
                    </div>
                  )}
                </div>

                {/* Message Actions */}
                <div className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
                  <button className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                    <MessageCircle size={14} />
                  </button>
                  <button className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                    <MoreVertical size={14} />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>

      {/* Typing Indicator */}
      {isTyping && (
        <div className="px-4 py-2 text-sm text-gray-500 dark:text-gray-400 italic">
          Someone is typing...
        </div>
      )}

      {/* Message Input */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4">
        <form onSubmit={handleSendMessage} className="flex items-end gap-3">
          <div className="flex-1">
            <div className="relative">
              <textarea
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder={`Message ${workspace.name}...`}
                className="w-full p-3 pr-12 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"
                rows={1}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage(e);
                  }
                }}
              />
              <button
                type="button"
                className="absolute bottom-3 right-3 p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                <Paperclip size={16} />
              </button>
            </div>
          </div>
          
          <button
            type="submit"
            disabled={!newMessage.trim()}
            className="px-4 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send size={16} />
          </button>
        </form>
      </div>
    </div>
  );
}

// Active Collaborators Component
function ActiveCollaborators({ workspace }: { workspace: Workspace }) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          Team ({workspace.members.length})
        </h3>
        <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
          <Settings size={16} />
        </button>
      </div>

      <div className="space-y-2">
        {workspace.members.map((member) => (
          <div key={member.id} className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800">
            <div className="relative">
              <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                {member.avatar ? (
                  <img 
                    src={member.avatar} 
                    alt={member.name}
                    className="w-8 h-8 rounded-full object-cover"
                  />
                ) : (
                  <User size={16} className="text-primary-600 dark:text-primary-400" />
                )}
              </div>
              <div className={`absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-white dark:border-gray-800 ${STATUS_COLORS[member.status]}`} />
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium text-gray-900 dark:text-white truncate">
                {member.name}
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                {member.status === 'online' ? 'Active now' : 
                 member.status === 'away' ? 'Away' :
                 `Last seen ${member.lastActive.toLocaleTimeString()}`}
              </div>
            </div>
            
            <div className="text-xs text-gray-400 px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">
              {member.role}
            </div>
          </div>
        ))}
      </div>

      {/* Invite Button */}
      <button className="w-full flex items-center justify-center gap-2 p-3 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg text-gray-500 dark:text-gray-400 hover:border-primary-300 hover:text-primary-600 dark:hover:border-primary-700 dark:hover:text-primary-400 transition-colors">
        <Plus size={16} />
        Invite team members
      </button>
    </div>
  );
}

export default function CollaborationPage() {
  const [selectedWorkspace, setSelectedWorkspace] = useState<Workspace | null>(DEMO_WORKSPACES[0]);
  const [messages, setMessages] = useState<Message[]>(DEMO_MESSAGES);
  const [activeTab, setActiveTab] = useState<string>('chat');
  const [isCreatingWorkspace, setIsCreatingWorkspace] = useState(false);
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const [isLoadingWorkspace, setIsLoadingWorkspace] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  // WebSocket connection
  useEffect(() => {
    const url = wsUrl();
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'message') {
          setMessages(prev => [...prev, data.message]);
        }
      } catch (error) {
        console.error('WebSocket message parsing error:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return () => {
      ws.close();
    };
  }, []);

  const handleSendMessage = useCallback((content: string, attachments?: File[]) => {
    if (!selectedWorkspace) return;

    const newMessage: Message = {
      id: `msg-${Date.now()}`,
      workspaceId: selectedWorkspace.id,
      userId: '1', // Current user ID
      userName: 'Dr. Sarah Chen', // Current user name
      content,
      type: 'text',
      timestamp: new Date(),
      attachments: attachments ? attachments.map(file => ({
        id: `att-${Date.now()}-${file.name}`,
        name: file.name,
        type: file.type,
        size: file.size,
        url: URL.createObjectURL(file)
      })) : []
    };

    // Add message locally
    setMessages(prev => [...prev, newMessage]);

    // Send via WebSocket
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'message',
        workspaceId: selectedWorkspace.id,
        message: newMessage
      }));
    }
  }, [selectedWorkspace]);

  const handleWorkspaceSelect = async (workspace: Workspace) => {
    setIsLoadingWorkspace(true);
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 500));
      setSelectedWorkspace(workspace);
      // Filter messages for selected workspace
      const workspaceMessages = DEMO_MESSAGES.filter(m => m.workspaceId === workspace.id);
      setMessages(workspaceMessages);
    } catch (error) {
      console.error('Error loading workspace:', error);
    } finally {
      setIsLoadingWorkspace(false);
    }
  };

  const handleCreateWorkspace = async () => {
    setIsCreatingWorkspace(true);
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log('Create new workspace');
      // In real implementation, this would create a workspace and refresh the list
    } catch (error) {
      console.error('Error creating workspace:', error);
    } finally {
      setIsCreatingWorkspace(false);
    }
  };

  const workspaceMessages = messages.filter(m => m.workspaceId === selectedWorkspace?.id);

  return (
    <DashboardLayout title="Collaboration" subtitle="Real-time workspace collaboration and communication">
      <div className="flex h-[calc(100vh-12rem)] max-w-7xl mx-auto gap-6">
        
        {/* Left Sidebar - Workspaces */}
        <div className="w-80 flex-shrink-0">
          <Panel className="h-full">
            <WorkspaceList
              workspaces={DEMO_WORKSPACES}
              selectedWorkspace={selectedWorkspace}
              onWorkspaceSelect={handleWorkspaceSelect}
              onCreateWorkspace={handleCreateWorkspace}
            />
          </Panel>
        </div>

        {/* Main Content */}
        <div className="flex-1 min-w-0">
          {selectedWorkspace ? (
            <Panel className="h-full">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="h-full flex flex-col">
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
                    <ChatInterface
                      workspace={selectedWorkspace}
                      messages={workspaceMessages}
                      onSendMessage={handleSendMessage}
                    />
                  </TabsContent>

                  <TabsContent value="documents" className="h-full m-0 p-4">
                    <div className="h-full flex items-center justify-center">
                      <div className="text-center">
                        <FolderOpen size={48} className="mx-auto text-gray-400 mb-4" />
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Document Sharing</h3>
                        <p className="text-gray-500 dark:text-gray-400">
                          Drag and drop files or click to upload documents to share with your team.
                        </p>
                        <button className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                          <Plus size={16} />
                          Upload Documents
                        </button>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="tasks" className="h-full m-0 p-4">
                    <div className="h-full flex items-center justify-center">
                      <div className="text-center">
                        <CheckCircle size={48} className="mx-auto text-gray-400 mb-4" />
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Task Management</h3>
                        <p className="text-gray-500 dark:text-gray-400">
                          Create and track tasks within your workspace for better project coordination.
                        </p>
                        <button className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
                          <Plus size={16} />
                          Create Task
                        </button>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="activity" className="h-full m-0 p-4">
                    <div className="h-full flex items-center justify-center">
                      <div className="text-center">
                        <Activity size={48} className="mx-auto text-gray-400 mb-4" />
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Activity Feed</h3>
                        <p className="text-gray-500 dark:text-gray-400">
                          Track all workspace activities, updates, and team interactions in real-time.
                        </p>
                      </div>
                    </div>
                  </TabsContent>
                </div>
              </Tabs>
            </Panel>
          ) : (
            <Panel className="h-full flex items-center justify-center">
              <div className="text-center">
                <Users size={48} className="mx-auto text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Select a Workspace</h3>
                <p className="text-gray-500 dark:text-gray-400">
                  Choose a workspace from the sidebar to start collaborating.
                </p>
              </div>
            </Panel>
          )}
        </div>

        {/* Right Sidebar - Team Members */}
        <div className="w-72 flex-shrink-0">
          <Panel className="h-full">
            {selectedWorkspace ? (
              <ActiveCollaborators workspace={selectedWorkspace} />
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
