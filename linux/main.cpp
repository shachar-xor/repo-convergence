extern "C"
{
    #include "weather.h"
}

#include <iostream>

int main()
{
    char buffer[1024];
    size_t bytes_written;
    get_weather(buffer, sizeof(buffer), &bytes_written);

    std::cout << buffer << std::endl;
}
