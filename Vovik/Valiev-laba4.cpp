#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <iomanip>

std::vector<double> exponentialModel(double x0, double r, int steps) {
    std::vector<double> result;
    double x = x0;
    for (int i = 0; i < steps; i++) {
        result.push_back(x);
        x = r * x;
    }
    return result;
}
std::vector<double> logisticModel(double x0, double r, int steps) {
    std::vector<double> result;
    double x = x0;
    for (int i = 0; i < steps; i++) {
        result.push_back(x);
        x = r * x * (1 - x);
    }
    return result;
}
std::vector<double> moranModel(double x0, double r, int steps) {
    std::vector<double> result;
    double x = x0;
    for (int i = 0; i < steps; i++) {
        result.push_back(x);
        x = x * std::exp(r * (1 - x));
    }
    return result;
}
std::pair<std::vector<double>, std::vector<double>> nicholsonBailey(
    double x0, double y0, double a, double b, double c, int steps) {
    std::vector<double> hosts, parasites;
    double x = x0, y = y0;
    for (int i = 0; i < steps; i++) {
        hosts.push_back(x);
        parasites.push_back(y);
        double x_next = b * x * std::exp(-a * y);
        double y_next = c * x * (1 - std::exp(-a * y));
        x = x_next;
        y = y_next;
    }
    return {hosts, parasites};
}
std::vector<double> findLogisticEquilibrium(double r) {
    std::vector<double> equilibria;
    equilibria.push_back(0.0);
    if (r > 1.0) {
        equilibria.push_back(1.0 - 1.0/r);
    }
    return equilibria;
}
bool checkStability(double x_star, double r) {
    double derivative = r * (1 - 2 * x_star);
    if (std::abs(derivative) < 1.0) {
        return true;
    } else {
        return false;
    }
}
void printAnalysisTable() {
    std::cout << "\nАнализ логистической модели:\n";
    std::cout << "r\tПоведение\t\tТочка равновесия\tУстойчивость\n";
    std::cout << "---------------------------------------------------------\n";
    std::vector<double> r_values = {0.5, 0.8, 1.5, 2.5, 2.9, 3.0, 3.2, 3.5, 3.8, 4.0};

    for (double r : r_values) {
        std::string behavior;
        std::string stability;
        if (r < 1.0) {
            behavior = "Вымрн";
        } else if (r < 3.0) {
            behavior = "Стабил";
        } else if (r < 3.449) {
            behavior = "2-цикл";
        } else if (r < 3.569) {
            behavior = "Сл цикл";
        } else {
            behavior = "Хаос";
        }
        auto eq_points = findLogisticEquilibrium(r);
        std::string eq_str = "";
        if (eq_points.size() > 0) {
            eq_str = std::to_string(eq_points[0]);
            if (eq_points.size() > 1) {
                eq_str = std::to_string(eq_points[1]);
            }
        }
        std::cout << r << "\t" << behavior << "\t\t" << eq_str << "\t\t";
        
        if (r < 3.0 && r > 1.0) {
            std::cout << "Устойч";
        } else {
            std::cout << "Неустойч";
        }
        std::cout << "\n";
    }
}
void saveToFile(const std::vector<double>& data, const std::string& filename) {
    std::ofstream file("output/" + filename);
    file << "time,population\n";
    for (size_t i = 0; i < data.size(); i++) {
        file << i << "," << data[i] << "\n";
    }
    file.close();
}
void saveTwoToFile(const std::vector<double>& x, const std::vector<double>& y, const std::string& filename) {
    std::ofstream file("output/" + filename);
    file << "time,hosts,parasites\n";
    for (size_t i = 0; i < x.size(); i++) {
        file << i << "," << x[i] << "," << y[i] << "\n";
    }
    file.close();
}
void generateData() {
    system("mkdir -p output");
    std::vector<double> stable_r = {0.8, 1.5, 2.5};
    for (double r : stable_r) {
        saveToFile(logisticModel(0.1, r, 50), "logistic_stable_r" + std::to_string((int)(r*10)) + ".csv");
    }
    std::vector<double> diff_r = {3.2, 3.5, 3.8, 4.0};
    for (double r : diff_r) {
        saveToFile(logisticModel(0.1, r, 100), "logistic_r" + std::to_string((int)(r*10)) + ".csv");
    }
    saveToFile(logisticModel(0.1, 2.9, 50), "critical_r29.csv");
    saveToFile(logisticModel(0.1, 3.1, 50), "critical_r31.csv");
    saveToFile(logisticModel(0.1, 3.55, 50), "critical_r355.csv");
    saveToFile(logisticModel(0.1, 3.6, 50), "critical_r36.csv");
    saveToFile(exponentialModel(0.1, 1.2, 30), "exponential_growth.csv");
    saveToFile(moranModel(0.5, 2.0, 50), "moran_model.csv");
    auto nb_stable = nicholsonBailey(0.5, 0.1, 0.1, 1.5, 1.0, 50);
    saveTwoToFile(nb_stable.first, nb_stable.second, "nb_stable.csv");
    auto nb_unstable = nicholsonBailey(0.5, 0.1, 0.5, 3.0, 1.0, 50);
    saveTwoToFile(nb_unstable.first, nb_unstable.second, "nb_unstable.csv");
    std::ofstream bif_file("output/bifurcation_data.csv");
    for (double r = 0.5; r <= 4.0; r += 0.01) {
        double x = 0.5;
        for (int i = 0; i < 200; i++) {
            x = r * x * (1 - x);
        }
        for (int i = 0; i < 50; i++) {
            x = r * x * (1 - x);
            bif_file << r << "," << x << "\n";
        }
    }
    bif_file.close();
    std::ofstream init_file("output/initial_dependence.csv");
    double r_chaos = 3.8;
    init_file << "time,x0=0.1,x0=0.2,x0=0.3,x0=0.4\n";
    for (int t = 0; t < 50; t++) {
        init_file << t;
        for (double x0 : {0.1, 0.2, 0.3, 0.4}) {
            double x = x0;
            for (int i = 0; i <= t; i++) {
                x = r_chaos * x * (1 - x);
            }
            init_file << "," << x;
        }
        init_file << "\n";
    }
    init_file.close();
}
void findCriticalValues() {
    std::cout << "\nКритические значения параметра r:\n";
    std::cout << "r = 1.0  - появление ненулевой точки равновесия\n";
    std::cout << "r = 3.0  - начало 2-цикла\n";
    std::cout << "r = 3.449 - начало 4-цикла\n";
    std::cout << "r = 3.569 - начало хаоса\n";
}
int main() {
    std::cout << std::fixed << std::setprecision(4);
    printAnalysisTable();
    findCriticalValues();
    generateData();
}