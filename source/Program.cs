using System;
using System.Threading;

class Program
{
    const int minTrail = 4;
    const int maxTrail = 12;

    static void Main()
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
        Console.CursorVisible = false;

        int width = Console.WindowWidth;
        int height = Console.WindowHeight;

        Random rand = new Random();

        // Each column will have a Y position and a trail length
        int[] yPositions = new int[width];
        int[] trailLengths = new int[width];

        for (int i = 0; i < width; i++)
        {
            yPositions[i] = rand.Next(height);
            trailLengths[i] = rand.Next(minTrail, maxTrail);
        }

        while (true)
        {
            for (int x = 0; x < width; x++)
            {
                int y = yPositions[x];

                // Draw head (bright white)
                Console.ForegroundColor = ConsoleColor.White;
                Console.SetCursorPosition(x, y);
                Console.Write((char)rand.Next(0x30A0, 0x30FF)); // Katakana characters

                // Draw trail (green)
                for (int j = 1; j < trailLengths[x]; j++)
                {
                    int trailY = (y - j + height) % height;
                    Console.ForegroundColor = ConsoleColor.DarkGreen;
                    Console.SetCursorPosition(x, trailY);
                    Console.Write((char)rand.Next(0x30A0, 0x30FF));
                }

                // Clean up old trail
                int eraseY = (y - trailLengths[x] + height) % height;
                Console.SetCursorPosition(x, eraseY);
                Console.Write(' ');

                // Update position
                yPositions[x] = (y + 1) % height;

                // Occasionally reset trail length for variety
                if (rand.NextDouble() < 0.01)
                {
                    trailLengths[x] = rand.Next(minTrail, maxTrail);
                }
            }

            Thread.Sleep(75); // ~13 fps, feels smooth-ish
        }
    }
}