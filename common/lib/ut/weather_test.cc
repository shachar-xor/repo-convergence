#include <gtest/gtest.h>

extern "C"
{
    #include "weather.h"
}

TEST(WeatherTest, BasicWeatherFetching) {
    char buffer[1024];
    size_t bytes_written;
    get_weather(buffer, sizeof(buffer), &bytes_written);

    EXPECT_LE(15, bytes_written);
    EXPECT_GE(200, bytes_written);
}

TEST(WeatherTest, InvalidWeatherFetching) {
    char buffer[1024];
    size_t bytes_written;
    get_weather(buffer, 0, &bytes_written);

    EXPECT_EQ(0, bytes_written);
}
