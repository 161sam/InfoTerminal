// Collaboration chat interface panel
import { useState, useEffect, useRef } from 'react';
import { 
  Search, 
  MoreVertical, 
  User, 
  Paperclip, 
  Download, 
  Smile, 
  MessageCircle, 
  Send 
} from 'lucide-react';
import { 
  Workspace, 
  Message, 
  WORKSPACE_COLORS,
  formatTimestamp,
  formatFileSize
} from '@/lib/collaboration/collab-config';

interface CollabChatInterfaceProps {
  workspace: Workspace;
  messages: Message[];
  onSendMessage: (content: string, attachments?: File[]) => void;
  onMessageAction?: (message: Message, action: string) => void;
}

export function CollabChatInterface({ 
  workspace, 
  messages, 
  onSendMessage,
  onMessageAction 
}: CollabChatInterfaceProps) {
  const [newMessage, setNewMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim() && selectedFiles.length === 0) return;

    onSendMessage(newMessage, selectedFiles.length > 0 ? selectedFiles : undefined);
    setNewMessage('');
    setSelectedFiles([]);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFiles(Array.from(e.target.files));
    }
  };

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const onlineCount = workspace.members.filter(m => m.status === 'online').length;
  const colorClass = WORKSPACE_COLORS[workspace.color as keyof typeof WORKSPACE_COLORS];
  const colorIndicator = colorClass.split(' ')[0]; // Extract just the background color

  return (
    <div className="flex flex-col h-full">
      {/* Chat Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className={`w-4 h-4 rounded-full ${colorIndicator}`} />
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">
              {workspace.name}
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {onlineCount} online
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <button 
            className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
            title="Search messages"
          >
            <Search size={16} />
          </button>
          <button 
            className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
            title="More options"
          >
            <MoreVertical size={16} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center py-8">
            <MessageCircle size={32} className="mx-auto text-gray-400 mb-2" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Start the conversation
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              Send a message to begin collaborating with your team.
            </p>
          </div>
        ) : (
          messages.map((message, index) => {
            const isConsecutive = index > 0 && 
              messages[index - 1].userId === message.userId &&
              (message.timestamp.getTime() - messages[index - 1].timestamp.getTime()) < 300000;

            return (
              <MessageBubble
                key={message.id}
                message={message}
                isConsecutive={isConsecutive}
                onAction={(action) => onMessageAction?.(message, action)}
              />
            );
          })
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Typing Indicator */}
      {isTyping && (
        <div className="px-4 py-2 text-sm text-gray-500 dark:text-gray-400 italic flex-shrink-0">
          Someone is typing...
        </div>
      )}

      {/* File Preview */}
      {selectedFiles.length > 0 && (
        <div className="px-4 py-2 border-t border-gray-200 dark:border-gray-700 flex-shrink-0">
          <div className="space-y-2">
            <p className="text-sm text-gray-700 dark:text-gray-300">
              {selectedFiles.length} file(s) selected:
            </p>
            <div className="space-y-1">
              {selectedFiles.map((file, index) => (
                <div key={index} className="flex items-center gap-2 p-2 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <Paperclip size={14} className="text-gray-400" />
                  <span className="text-sm text-gray-700 dark:text-gray-300 flex-1 truncate">
                    {file.name}
                  </span>
                  <span className="text-xs text-gray-500">
                    {formatFileSize(file.size)}
                  </span>
                  <button
                    onClick={() => removeFile(index)}
                    className="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Message Input */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4 flex-shrink-0">
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
              <input
                ref={fileInputRef}
                type="file"
                multiple
                onChange={handleFileSelect}
                className="hidden"
              />
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="absolute bottom-3 right-3 p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                title="Attach files"
              >
                <Paperclip size={16} />
              </button>
            </div>
          </div>
          
          <button
            type="submit"
            disabled={!newMessage.trim() && selectedFiles.length === 0}
            className="px-4 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            title="Send message"
          >
            <Send size={16} />
          </button>
        </form>
      </div>
    </div>
  );
}

interface MessageBubbleProps {
  message: Message;
  isConsecutive: boolean;
  onAction: (action: string) => void;
}

function MessageBubble({ message, isConsecutive, onAction }: MessageBubbleProps) {
  return (
    <div className={`group ${isConsecutive ? 'ml-12' : ''}`}>
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
              {message.edited && (
                <span className="text-xs text-gray-400 italic">
                  (edited)
                </span>
              )}
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
                    {formatFileSize(attachment.size)}
                  </span>
                  <button 
                    onClick={() => window.open(attachment.url, '_blank')}
                    className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                    title="Download file"
                  >
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
                  onClick={() => onAction(`react:${reaction.emoji}`)}
                  className="inline-flex items-center gap-1 px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                >
                  <span>{reaction.emoji}</span>
                  <span className="text-gray-600 dark:text-gray-400">
                    {reaction.count}
                  </span>
                </button>
              ))}
              <button 
                onClick={() => onAction('add_reaction')}
                className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity"
                title="Add reaction"
              >
                <Smile size={14} />
              </button>
            </div>
          )}
        </div>

        {/* Message Actions */}
        <div className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
          <button 
            onClick={() => onAction('reply')}
            className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            title="Reply in thread"
          >
            <MessageCircle size={14} />
          </button>
          <button 
            onClick={() => onAction('more')}
            className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            title="More actions"
          >
            <MoreVertical size={14} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default CollabChatInterface;
