#include <deque>
#include <string>
#include <vector>
#include <cmath>

struct MarketEvent {
    std::string symbol;
    double price;
    double volume;
};

struct SignalResult {
    double score;
    std::vector<std::string> reasons;
};

class SignalEngine {
private:
    std::deque<double> prices;
    std::deque<double> volumes;
    const size_t WINDOW_SIZE = 10;

public:
    SignalResult process(const MarketEvent& event) {
        prices.push_back(event.price);
        volumes.push_back(event.volume);

        if (prices.size() > WINDOW_SIZE) {
            prices.pop_front();
            volumes.pop_front();
        }

        SignalResult result{0.0, {}};

        if (prices.size() < WINDOW_SIZE)
            return result;

        // ---- Price Momentum ----
        double momentum = prices.back() - prices.front();
        if (std::abs(momentum) > 5.0) {
            result.score += 30;
            result.reasons.push_back("momentum");
        }

        // ---- Volume Spike ----
        double avg_volume = 0;
        for (double v : volumes) avg_volume += v;
        avg_volume /= volumes.size();

        if (event.volume > 3 * avg_volume) {
            result.score += 40;
            result.reasons.push_back("volume_spike");
        }

        // ---- Volatility ----
        double mean_price = 0;
        for (double p : prices) mean_price += p;
        mean_price /= prices.size();

        double variance = 0;
        for (double p : prices)
            variance += (p - mean_price) * (p - mean_price);
        variance /= prices.size();

        if (variance > 10) {
            result.score += 30;
            result.reasons.push_back("volatility");
        }

        return result;
    }
};
