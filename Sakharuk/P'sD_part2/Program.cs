using ConsoleTables;

namespace P_sD_part2
{
    internal class Program
    {
        private static readonly int[,] winTable = new int[,] { { 3, 0 }, { 5, 1 } };
        private static readonly string[] names = ["Alex", "Bob", "Clara", "Denis", "Emma", "Frida", "George", "Hank", "Ivan", "Jack", "Kevin", "Lucas", "Max", "Natan"];
        private static readonly int playersCount = 14;
        private static readonly int totalRoundCount = 50;
        private static readonly int roundCount = 200;
        private static readonly byte one = 1;
        private static readonly byte zero = 0;

        private static readonly Random rnd = new();
        private static int lucasRnd = rnd.Next(1, 50);
        private static int maxRnd = rnd.Next(0, 20);
        private static byte maxMove = zero;
        private static int maxIndex = 0;

        public static int[,] Tournament(out double[] averagePerGame, out int[,] series, out double[,] dispersion, out int[,] medians, out double[,] modes)
        {
            averagePerGame = new double[playersCount];
            dispersion = new double[playersCount, playersCount];
            medians = new int[playersCount, playersCount];
            modes = new double[playersCount, playersCount];
            int[,] result = new int[playersCount, playersCount];
            series = new int[playersCount, playersCount];

            for (int first = 0; first < playersCount; first++)
            {
                for (int second = first + 1; second < playersCount; second++)
                {
                    int totalFirstScore = 0, totalSecondScore = 0;

                    int[] firstPlayerGameScores = new int[totalRoundCount];
                    int[] secondPlayerGameScores = new int[totalRoundCount];

                    for (int game = 0; game < totalRoundCount; game++)
                    {
                        int firstScore = 0, secondScore = 0;

                        byte lastFirstMove = 0, lastSecondMove = 0;
                        bool firstOpponentDefected = false, secondOpponentDefected = false;

                        int currentSeries1 = 0, currentSeries2 = 0;
                        int maxSeries1 = 0, maxSeries2 = 0;

                        for (int round = 0; round < roundCount; round++)
                        {
                            bool isTwenties = (round % 20 == 0);

                            byte move1 = MakeMove(first, round == 0, isTwenties, firstOpponentDefected, lastSecondMove, round);
                            byte move2 = MakeMove(second, round == 0, isTwenties, secondOpponentDefected, lastFirstMove, round);
                            Round(move1, move2, out int delta1, out int delta2);

                            firstScore += delta1;
                            secondScore += delta2;

                            if (delta1 == 5 && delta2 == 0)
                            {
                                currentSeries1++;
                                currentSeries2 = 0;
                                if (currentSeries1 > maxSeries1) maxSeries1 = currentSeries1;
                            }
                            else if (delta1 == 0 && delta2 == 5)
                            {
                                currentSeries2++;
                                currentSeries1 = 0;
                                if (currentSeries2 > maxSeries2) maxSeries2 = currentSeries2;
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


                        lucasRnd = rnd.Next(1, 50);
                        maxIndex = 0;

                        firstPlayerGameScores[game] = firstScore;
                        secondPlayerGameScores[game] = secondScore;

                        totalFirstScore += firstScore;
                        totalSecondScore += secondScore;

                        series[first, second] = Math.Max(series[first, second], maxSeries1);
                        series[second, first] = Math.Max(series[second, first], maxSeries2);
                    }

                    dispersion[first, second] = Dispersion(firstPlayerGameScores);
                    dispersion[second, first] = Dispersion(secondPlayerGameScores);

                    medians[first, second] = Median(firstPlayerGameScores);
                    medians[second, first] = Median(secondPlayerGameScores);

                    modes[first, second] = Mode(firstPlayerGameScores);
                    modes[second, first] = Mode(secondPlayerGameScores);

                    result[first, second] = totalFirstScore / totalRoundCount;
                    result[second, first] = totalSecondScore / totalRoundCount;

                    averagePerGame[first] += totalFirstScore;
                    averagePerGame[second] += totalSecondScore;
                }
            }

            for (int i = 0; i < playersCount; i++)
            {
                averagePerGame[i] = averagePerGame[i] / (playersCount - 1) / totalRoundCount;
            }

            return result;
        }

        private static double Dispersion(int[] values)
        {
            if (values.Length == 0) return 0;
            if (values.Length == 1) return 0;

            double mean = values.Average();
            double sumSquaredDifferences = 0;

            foreach (int value in values)
            {
                double difference = value - mean;
                sumSquaredDifferences += difference * difference;
            }

            return sumSquaredDifferences / values.Length;
        }

        private static int Median(int[] values)
        {
            if (values.Length == 0) return 0;

            int[] sorted = [.. values.OrderBy(v => v)];

            if (sorted.Length % 2 == 1)
                return sorted[sorted.Length / 2];
            else
                return (sorted[sorted.Length / 2 - 1] + sorted[sorted.Length / 2]) / 2;
        }

        private static double Mode(int[] values)
        {
            if (values.Length == 0) return 0;

            if (values.All(v => v == values[0]))
                return values[0];

            int k = (int)Math.Ceiling(Math.Log(1 + values.Length, 2));

            int min = values.Min();
            int max = values.Max();

            double intervalWidth = (max - min) / (double)k;

            int[] frequencies = new int[k];

            foreach (int value in values)
            {
                int intervalIndex = (int)((value - min) / intervalWidth);
                if (intervalIndex >= k) intervalIndex = k - 1;
                frequencies[intervalIndex]++;
            }

            int maxFrequencyIndex = 0;
            int maxFrequency = frequencies[0];
            for (int i = 1; i < k; i++)
            {
                if (frequencies[i] > maxFrequency)
                {
                    maxFrequency = frequencies[i];
                    maxFrequencyIndex = i;
                }
            }

            double modalIntervalStart = min + maxFrequencyIndex * intervalWidth;
            double modalIntervalEnd = modalIntervalStart + intervalWidth;

            List<int> modalValues = [];
            foreach (int value in values)
            {
                if (value >= modalIntervalStart &&
                    (value < modalIntervalEnd || (value == max && maxFrequencyIndex == k - 1)))
                {
                    modalValues.Add(value);
                }
            }

            return modalValues.Count > 0 ? modalValues.Average() : (modalIntervalStart + modalIntervalEnd) / 2;
        }
        private static void Round(int first, int second, out int firstScore, out int secondScore)
        {
            firstScore = winTable[first, second];
            secondScore = winTable[second, first];
        }

        private static byte MakeMove(int indexOfPlayer, bool isFirst, bool isTwenties, bool firstOpponentDefected, byte lastOpponentMove, int indexOfMatch)
        {
            return indexOfPlayer switch
            {
                0 => Alex(),
                1 => Bob(),
                2 => Clara(isFirst, lastOpponentMove),
                3 => Denis(isFirst, lastOpponentMove),
                4 => Emma(isTwenties),
                5 => Frida(firstOpponentDefected),
                6 => George(isFirst),
                7 => Hank(),
                8 => Ivan(),
                9 => Jack(isFirst, lastOpponentMove),
                10 => Kevin(isFirst, lastOpponentMove),
                11 => Lucas(indexOfMatch),
                12 => Max(),
                13 => Natan(isFirst, lastOpponentMove),
                _ => throw new ArgumentException($"Undefined player: {indexOfPlayer}")
            };
        }

        private static byte Hank() => (byte)rnd.Next(2);
        private static byte Ivan() => rnd.NextDouble() < 0.9 ? zero : one;
        private static byte Jack(bool isFirst, byte lastOpponentMove) => isFirst ?
            zero : (lastOpponentMove == 0 ? zero : (rnd.NextDouble() < 0.25 ? zero : one));
        private static byte Kevin(bool isFirst, byte lastOpponentMove) => (byte)(isFirst ?
            zero : (rnd.NextDouble() < 0.25 ? ((byte)(1) - lastOpponentMove) : lastOpponentMove));
        private static byte Lucas(int match) => match % lucasRnd == 0 ? one : zero;
        private static byte Max()
        {
            if (maxRnd <= maxIndex)
            {
                maxRnd = rnd.Next(0, 20);
                maxMove = maxMove == one ? zero : one;
                maxIndex = 0;
            }
            maxIndex++;
            return maxMove;
        }
        private static byte Natan(bool isFirst, byte lastOpponent)
        {
            if (isFirst)
                return zero;
            double q = rnd.NextDouble();
            if (lastOpponent == one)
                return q > 0.7 ? zero : one;
            return zero;
        }

        private static byte Alex() => 1;
        private static byte Bob() => 0;
        private static byte Clara(bool isFirst, byte lastOpponent) => isFirst ? zero : lastOpponent;
        private static byte Denis(bool isFirst, byte lastOpponent) => isFirst ? zero : (byte)(one - lastOpponent);
        private static byte Emma(bool isTwenties) => isTwenties ? one : zero;
        private static byte Frida(bool opponentDefected) => opponentDefected ? one : zero;
        private static byte George(bool isFirst) => isFirst ? one : zero;

        static void Main()
        {
            try
            {
                int[,] result = Tournament(out double[] averagePerGame, out int[,] series, out double[,] varianceBetweenPlayers, out int[,] medians, out double[,] modes);
                DisplayAverageScore(result, averagePerGame, names);
                DisplayDispersionTable(varianceBetweenPlayers, names);
                DisplayMedianTable(medians, names);
                DisplayModeTable(modes, names);
            }
            catch (Exception e)
            {
                Console.Error.WriteLine(e.Message);
            }
        }

        private static void DisplayAverageScore(int[,] result, double[] averagePerGame, string[] names)
        {
            var headers = new List<string> { "first\\second" };
            headers.AddRange(names);
            headers.Add("Average");
            var table = new ConsoleTable([.. headers]);
            for (int i = 0; i < names.Length; i++)
            {
                var row = new List<object> { names[i] };

                for (int j = 0; j < names.Length; j++)
                {
                    if (i == j)
                        row.Add("-");
                    else
                        row.Add(result[i, j]);
                }
                row.Add(Math.Round(averagePerGame[i], 2));
                table.AddRow([.. row]);
            }
            table.Write(Format.Alternative);
            Console.WriteLine();
        }

        private static void DisplayDispersionTable(double[,] varianceBetweenPlayers, string[] names)
        {
            Console.WriteLine("Dispersion");

            var headers = new List<string> { "first\\second" };
            headers.AddRange(names);
            var table = new ConsoleTable([.. headers]);

            for (int i = 0; i < names.Length; i++)
            {
                var row = new List<object> { names[i] };

                for (int j = 0; j < names.Length; j++)
                {
                    if (i == j)
                        row.Add("-");
                    else
                        row.Add(Math.Round(varianceBetweenPlayers[i, j], 2));
                }
                table.AddRow([.. row]);
            }
            table.Write(Format.Alternative);
            Console.WriteLine();
        }

        private static void DisplayMedianTable(int[,] medians, string[] names)
        {
            Console.WriteLine("Median");

            var headers = new List<string> { "first\\second" };
            headers.AddRange(names);
            var table = new ConsoleTable([.. headers]);

            for (int i = 0; i < names.Length; i++)
            {
                var row = new List<object> { names[i] };

                for (int j = 0; j < names.Length; j++)
                {
                    if (i == j)
                        row.Add("-");
                    else
                        row.Add(medians[i, j]);
                }
                table.AddRow([.. row]);
            }
            table.Write(Format.Alternative);
            Console.WriteLine();
        }

        private static void DisplayModeTable(double[,] modes, string[] names)
        {
            Console.WriteLine("Modes (Most Frequent Score Range)");

            var headers = new List<string> { "first\\second" };
            headers.AddRange(names);
            var table = new ConsoleTable([.. headers]);

            for (int i = 0; i < names.Length; i++)
            {
                var row = new List<object> { names[i] };

                for (int j = 0; j < names.Length; j++)
                {
                    if (i == j)
                        row.Add("-");
                    else
                        row.Add(Math.Round(modes[i, j], 2));
                }
                table.AddRow([.. row]);
            }
            table.Write(Format.Alternative);
            Console.WriteLine();
        }
    }
}