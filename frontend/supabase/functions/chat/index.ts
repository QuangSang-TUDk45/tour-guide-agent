const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

Deno.serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { messages, conversationId } = await req.json();
    
    if (!messages || !Array.isArray(messages)) {
      throw new Error('Messages array is required');
    }

    const GEMINI_API_KEY = "AIzaSyDKC_32qtWFE2H3xOXIgN8PSJc2qIgsLrQ";
    if (!GEMINI_API_KEY) {
      throw new Error('GEMINI_API_KEY is not configured');
    }

    console.log(`Processing chat request for conversation: ${conversationId}`);
    console.log(`Number of messages: ${messages.length}`);

    // Format messages for Gemini API
    const formattedMessages = messages.map((msg: ChatMessage) => ({
      role: msg.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: msg.content }],
    }));

    // Add system prompt at the beginning
    const systemPrompt = {
      role: 'user',
      parts: [{
        text: 'Bạn là trợ lý du lịch AI thông minh và thân thiện, chuyên tư vấn về các địa điểm du lịch Việt Nam. Bạn có khả năng:\n' +
              '- Gợi ý các địa điểm tham quan phù hợp với sở thích người dùng\n' +
              '- Lên kế hoạch chi tiết cho chuyến đi (lịch trình theo ngày)\n' +
              '- Tư vấn về khách sạn, nhà hàng, phương tiện di chuyển\n' +
              '- Cung cấp thông tin về văn hóa, ẩm thực địa phương\n' +
              '- Ước tính chi phí và ngân sách cho chuyến đi\n\n' +
              'Hãy trả lời một cách nhiệt tình, chi tiết và hữu ích.'
      }]
    };

    const allMessages = [systemPrompt, ...formattedMessages];

    // Call Gemini API with streaming
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:streamGenerateContent?key=${GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: allMessages,
          generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 2048,
          },
          safetySettings: [
            {
              category: 'HARM_CATEGORY_HARASSMENT',
              threshold: 'BLOCK_MEDIUM_AND_ABOVE',
            },
            {
              category: 'HARM_CATEGORY_HATE_SPEECH',
              threshold: 'BLOCK_MEDIUM_AND_ABOVE',
            },
            {
              category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
              threshold: 'BLOCK_MEDIUM_AND_ABOVE',
            },
            {
              category: 'HARM_CATEGORY_DANGEROUS_CONTENT',
              threshold: 'BLOCK_MEDIUM_AND_ABOVE',
            },
          ],
        }),
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Gemini API error:', response.status, errorText);
      throw new Error(`Gemini API error: ${response.status}`);
    }

    // Stream the response back to the client
    const stream = new ReadableStream({
      async start(controller) {
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
          controller.close();
          return;
        }

        try {
          while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
              controller.close();
              break;
            }

            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n');

            for (const line of lines) {
              if (line.trim() === '' || line.trim() === '[') continue;
              
              try {
                // Remove trailing comma if present
                const cleanLine = line.trim().replace(/,$/, '');
                if (cleanLine === '') continue;
                
                const data = JSON.parse(cleanLine);
                
                if (data.candidates && data.candidates[0]?.content?.parts) {
                  const text = data.candidates[0].content.parts[0]?.text;
                  if (text) {
                    // Send as SSE format
                    const sseData = `data: ${JSON.stringify({ text })}\n\n`;
                    controller.enqueue(new TextEncoder().encode(sseData));
                  }
                }
              } catch (e) {
                // Skip invalid JSON lines
                console.warn('Failed to parse line:', line, e);
              }
            }
          }
        } catch (error) {
          console.error('Stream error:', error);
          controller.error(error);
        }
      },
    });

    return new Response(stream, {
      headers: {
        ...corsHeaders,
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });

  } catch (error) {
    console.error('Chat function error:', error);
    return new Response(
      JSON.stringify({ 
        error: error instanceof Error ? error.message : 'Unknown error occurred' 
      }),
      {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  }
});
