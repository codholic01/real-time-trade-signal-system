#include "httplib.h"
#include "signal_engine.cpp"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
    httplib::Server server;
    SignalEngine engine;

    server.Post("/event", [&](const httplib::Request& req,
                              httplib::Response& res) {

        auto data = json::parse(req.body);

        MarketEvent event{
            data["symbol"],
            data["price"],
            data["volume"]
        };

        SignalResult result = engine.process(event);

        json response;
        response["symbol"] = event.symbol;
        response["signal_score"] = result.score;
        response["reasons"] = result.reasons;

        res.set_content(response.dump(), "application/json");
    });

    server.listen("0.0.0.0", 18080);
}
