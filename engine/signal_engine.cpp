#include <iostream>
#include <deque>
#include <string>

struct MarketEvent {
    std::string symbol;
    double price;
};

class SignalEngine {
private:
    std::deque<double> prices;
    const size_t WINDOW_SIZE = 5;

public:
    double process_event(const MarketEvent& event) {
        prices.push_back(event.price);
        if (prices.size() > WINDOW_SIZE) {
            prices.pop_front();
        }

        if (prices.size() < WINDOW_SIZE) {
            return 0.0;
        }

        double momentum = prices.back() - prices.front();
        return momentum;
    }
};

int main() {
    SignalEngine engine;

    // Simulated events (later comes from Python)
    double sample_prices[] = {43000, 43100, 43250, 43300, 43500};

    for (double price : sample_prices) {
        MarketEvent event{"BTCUSDT", price};
        double signal = engine.process_event(event);
        std::cout << "Price: " << price
                  << " | Signal score: " << signal << std::endl;
    }

    return 0;
}
