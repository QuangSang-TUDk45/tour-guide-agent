import { useState, useRef, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Send, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { v4 as uuidv4 } from 'uuid';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { addMessage, updateLastMessage, setLoading, setConversationId } from '@/store/slices/chatSlice';
import { RootState } from '@/store';
import ChatMessage from './ChatMessage';
import { toast } from '@/hooks/use-toast';
import { chatAPI } from '@/services/api';

const ChatInterface = () => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const dispatch = useDispatch();
  const { conversationId, messages, isLoading } = useSelector((state: RootState) => state.chat);

  // Initialize conversation ID on mount
  useEffect(() => {
    if (!conversationId) {
      dispatch(setConversationId(uuidv4()));
    }
  }, [conversationId, dispatch]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: uuidv4(),
      role: 'user' as const,
      content: inputValue,
      timestamp: new Date(),
    };

    dispatch(addMessage(userMessage));
    const currentInput = inputValue;
    setInputValue('');
    dispatch(setLoading(true));

    try {
      // Create initial assistant message
      const assistantMessage = {
        id: uuidv4(),
        role: 'assistant' as const,
        content: '',
        timestamp: new Date(),
        componentType: 'text' as const,
      };
      dispatch(addMessage(assistantMessage));

      // Call the backend API
      const response = await chatAPI.sendMessage(currentInput);
      const assistantContent = response.data.data || 'Không nhận được phản hồi từ hệ thống.';

      dispatch(updateLastMessage(assistantContent));
    } catch (error) {
      console.error('Error sending message:', error);
      toast({
        title: 'Lỗi',
        description: 'Không thể gửi tin nhắn. Vui lòng thử lại.',
        variant: 'destructive',
      });
      dispatch(updateLastMessage('Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu của bạn.'));
    } finally {
      dispatch(setLoading(false));
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        <AnimatePresence initial={false}>
          {messages.map((message, index) => (
            <ChatMessage key={message.id} message={message} index={index} />
          ))}
        </AnimatePresence>

        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center gap-2 text-muted-foreground"
          >
            <Loader2 className="h-4 w-4 animate-spin" />
            <span className="text-sm">Trợ lý đang suy nghĩ...</span>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t bg-card p-4">
        <div className="flex gap-2 max-w-4xl mx-auto">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Nhập tin nhắn của bạn..."
            className="flex-1"
            disabled={isLoading}
          />
          <Button
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim()}
            className="gradient-ocean"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>

        {/* Quick Actions */}
        <div className="flex flex-wrap gap-2 mt-3 max-w-4xl mx-auto">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setInputValue('Gợi ý chuyến đi cuối tuần')}
            className="text-xs"
          >
            🌴 Chuyến đi cuối tuần
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setInputValue('Tìm khách sạn ở Quy Nhơn')}
            className="text-xs"
          >
            🏨 Tìm khách sạn
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setInputValue('Lên kế hoạch 3 ngày ở Quy Nhơn')}
            className="text-xs"
          >
            ✈️ Lên kế hoạch
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
