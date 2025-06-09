using System;
using System.Collections.Generic;
using System.Threading;

class Program
{
    class Stream
    {
        public int X;
        public float Y;
        public float Speed;
        public int TrailLength;
        public int Delay;
        public int Height;
        public Queue<int> Trail = new();

        private static Random rand = new Random();

        public Stream(int x, int screenHeight)
        {
            X = x;
            Height = screenHeight;
            Reset();
        }

        public void Reset()
        {
            Y = rand.Next(-Height, 0);
            Speed = (float)(0.5 + rand.NextDouble() * 1.5);
            TrailLength = rand.Next(6, 20);
            Delay = rand.Next(0, 50);
            Trail.Clear();
        }

        public void Update()
        {
            if (Delay > 0)
            {
                Delay--;
                return;
            }

            Y += Speed;

            if (Y >= Height + TrailLength)
                Reset();
        }

        public void Draw()
        {
            if (Delay > 0) return;

            for (int i = 0; i < TrailLength; i++)
            {
                int yPos = (int)(Y - i);
                if (yPos < 0 || yPos >= Height) continue;

                Console.SetCursorPosition(X, yPos);

                if (i == 0)
                {
                    Console.ForegroundColor = ConsoleColor.White;
                }
                else if (i < TrailLength / 3)
                {
                    Console.ForegroundColor = ConsoleColor.Green;
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.DarkGreen;
                }

                char c = (char)(rand.Next(0x30A0, 0x30FF));
                Console.Write(c);
            }

            // Erase one below trail
            int clearY = (int)(Y - TrailLength);
            if (clearY >= 0 && clearY < Height)
            {
                Console.SetCursorPosition(X, clearY);
                Console.Write(' ');
            }
        }
    }

    static void Main()
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
        Console.CursorVisible = false;

        int width = Console.WindowWidth;
        int height = Console.WindowHeight;

        List<Stream> streams = new();
        for (int x = 0; x < width; x++)
        {
            if (new Random().NextDouble() < 0.6) // 60% of columns active
            {
                streams.Add(new Stream(x, height));
            }
        }

        while (true)
        {
            foreach (var stream in streams)
            {
                stream.Update();
                stream.Draw();
            }

            Thread.Sleep(33); // ~30 FPS
        }
    }
}
