using ConsoleTables;
using System.Collections.ObjectModel;

namespace Prisoner_sDilemma
{
    internal class Program
    {
        private static readonly int[,] winTable = new int[,] { { 3, 0 }, { 5, 1 } };
        private static readonly string[] names = ["Alex", "Bob", "Clara", "Denis", "Emma", "Frida", "George"];
        private static readonly int playersCount = 7;
        private static readonly int roundCount = 200;

        public static int[,] Game200(out int[] total, out int[,] series)
        {
            total = new int[playersCount];
            int[,] result = new int[playersCount, playersCount];
            series = new int[playersCount, playersCount];

            for (int first = 0; first < playersCount; first++)
            {
                for (int second = first + 1; second < playersCount; second++)
                {
                    int firstScore = 0, secondScore = 0;

                    int lastFirstMove = 0, lastSecondMove = 0;

                    bool firstOpponentDefected = false, secondOpponentDefected = false;

                    int currentSeries1 = 0, currentSeries2 = 0;
                    int maxSeries1 = 0, maxSeries2 = 0;

                    for (int i = 0; i < roundCount; i++)
                    {
                        bool isTwenties = (i % 20 == 0);

                        int move1 = MakeMove(first, i == 0, isTwenties, firstOpponentDefected, lastSecondMove);
                        int move2 = MakeMove(second, i == 0, isTwenties, secondOpponentDefected, lastFirstMove);
                        Round(move1, move2, out int delta1, out int delta2);

                        firstScore += delta1;
                        secondScore += delta2;

                        if (delta1 == 5 && delta2 == 0)
                        {
                            currentSeries1++;
                            currentSeries2 = 0;
                            if (currentSeries1 > maxSeries1)
                                maxSeries1 = currentSeries1;
                        }
                        else if (delta1 == 0 && delta2 == 5)
                        {
                            currentSeries2++;
                            currentSeries1 = 0;
                            if (currentSeries2 > maxSeries2)
                                maxSeries2 = currentSeries2;
                        }
                        else
                        {
                            currentSeries1 = 0;
                            currentSeries2 = 0;
                        }

                        firstOpponentDefected = (move2 == 1);
                        secondOpponentDefected = (move1 == 1);

                        lastFirstMove = move1;
                        lastSecondMove = move2;


                    }

                    result[first, second] = firstScore;
                    result[second, first] = secondScore;
                    total[first] += firstScore;
                    total[second] += secondScore;

                    series[first, second] = maxSeries1;
                    series[second, first] = maxSeries2;
                }
            }
            return result;
        }
        private static void Round(int first, int second, out int firstScore,out int secondScore)
        {
            firstScore = winTable[first, second];
            secondScore = winTable[second, first];
        }

        private static int MakeMove(int indexOfPlayer, bool isFirst, bool isTwenties, bool firstOpponentDefected, int lastOpponentMove)
        {
            return indexOfPlayer switch
            {
                0 => Alex(),
                1 => Bob(),
                2 => Clara(isFirst, lastOpponentMove),
                3 => Denis(isFirst, lastOpponentMove),
                4 => Emma(isTwenties),
                5 => Frida(firstOpponentDefected),
                6 => George(),
                _ => throw new ArgumentException($"Undefined player: {indexOfPlayer}")
            };
        }
        private static int Alex() => 1;
        private static int Bob() => 0;
        private static int Clara(bool isFirst, int lastOpponent) => isFirst ? 0 : lastOpponent;
        private static int Denis(bool isFirst, int lastOpponent) => isFirst ? 0 : (1 - lastOpponent);
        private static int Emma(bool isTwenties) => isTwenties ? 1 : 0;
        private static int Frida(bool opponentDefected) => opponentDefected ? 1 : 0;
        private static int George()
        {
            Random rnd = new();
            return rnd.Next(0, 2);
        }
         private static void DisplayResultTable(int[,] result, int[] total, string[] names)
        {
            var headers = new List<string> { "first\\second" };
            headers.AddRange(names);
            headers.Add("Total");
            var table = new ConsoleTable([..headers]);
            for (int i = 0; i < names.Length; i++)
            {
                var row = new List<object> { names[i] };

                for (int j = 0; j < names.Length; j++)
                {
                    row.Add(result[i, j]);
                }
                row.Add(total[i]);
                table.AddRow([..row]);
            }
            table.Write(Format.Alternative);
        }

        private static void DisplaySerieTable(int[,] series, string[] names)
        {
            var headers = new List<string> { "first\\second" };
            headers.AddRange(names);
            var table = new ConsoleTable([.. headers]);
            for (int i = 0; i < names.Length; i++)
            {
                var row = new List<object> { names[i] };

                for (int j = 0; j < names.Length; j++)
                {
                    row.Add(series[i, j]);
                }
                table.AddRow([.. row]);
            }
            table.Write(Format.Alternative);
        }

        static void Main()
        {
            try
            {
                int[,] result = Game200(out int[] total, out int[,] series);
                DisplayResultTable(result, total, names);
                DisplaySerieTable(series, names);

            }
            catch (Exception e)
            {
                Console.Error.WriteLine(e.Message);
            }
        }
    }
}
