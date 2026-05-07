import { CopilotProvider } from '@copilotkit/react-core';
import { CopilotTextarea } from '@copilotkit/react-textarea';
import { CopilotKitConfig, useMakeCopilotReadable } from '@copilotkit/react-core';
import { useChat } from 'ai';

const copilotKitConfig: CopilotKitConfig = {
  publicApiKey: process.env.VITE_COPILOTKIT_PUBLIC_API_KEY || '',
  serviceUrl: process.env.VITE_API_URL || 'http://localhost:8000',
};

// This is a wrapper component for CopilotKit integration
// Note: This is a placeholder as we're building a custom UI
// In a full implementation, you would integrate CopilotKit here

export function CopilotKitWrapper({ children }: { children: React.ReactNode }) {
  return (
    <CopilotProvider
      runtimeUrl={copilotKitConfig.serviceUrl}
      publicApiKey={copilotKitConfig.publicApiKey}
    >
      {children}
    </CopilotProvider>
  );
}

export function LangGraphChatAdapter() {
  const { messages, input, setInput, append, isLoading } = useChat({
    api: `${copilotKitConfig.serviceUrl}/chat`,
  });

  useMakeCopilotReadable(messages);

  return {
    messages,
    input,
    setInput,
    sendMessage: append,
    isLoading,
  };
}

// Custom hook for agent interaction
export function useLangGraphAgent() {
  const sendMessage = async (message: string, useStream = false) => {
    if (useStream) {
      const eventSource = new EventSource(
        `${copilotKitConfig.serviceUrl}/stream?message=${encodeURIComponent(message)}`
      );

      return new Promise((resolve, reject) => {
        let fullResponse = '';

        eventSource.onmessage = (event) => {
          const data = JSON.parse(event.data);
          if (data.type === 'chunk') {
            fullResponse += data.content;
          } else if (data.type === 'complete') {
            fullResponse = data.content;
            eventSource.close();
            resolve(fullResponse);
          } else if (data.type === 'error') {
            eventSource.close();
            reject(new Error(data.content));
          }
        };

        eventSource.onerror = () => {
          eventSource.close();
          reject(new Error('Connection error'));
        };
      });
    } else {
      const response = await fetch(`${copilotKitConfig.serviceUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [{ role: 'user', content: message }],
        }),
      });
      const data = await response.json();
      return data.response;
    }
  };

  return { sendMessage };
}
