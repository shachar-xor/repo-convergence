#include "weather.h"

#include <stdio.h>
#include <stdlib.h>
#include <memory.h>

#include <curl/curl.h>

struct MemoryStruct {
  char *memory;
  size_t curr_size;
  size_t buffer_total_size;
};

static size_t
WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
    size_t realsize = size * nmemb;

    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    if (mem->curr_size + realsize > mem->buffer_total_size)
    {
        fprintf(stderr, "Buffer too small");
        return 0;
    }

    memcpy(&(mem->memory[mem->curr_size]), contents, realsize);
    mem->curr_size += realsize;
    mem->memory[mem->curr_size] = 0;

    return realsize;
}

void get_weather(char* buffer, size_t buffer_size, size_t* bytes_written)
{
    *bytes_written = 0;

    struct MemoryStruct chunk;

    chunk.memory = buffer;
    chunk.curr_size = 0;
    chunk.buffer_total_size = buffer_size;

    CURL *curl;
    CURLcode res;

    curl = curl_easy_init();
    if(!curl)
    {
      fprintf(stderr, "curl_easy_init()");
      return;
    }

    curl_easy_setopt(curl, CURLOPT_URL, "http://wttr.in/?format=3");
    /* example.com is redirected, so we tell libcurl to follow redirection */
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

    /* send all data to this function  */
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);

    /* we pass our 'chunk' struct to the callback function */
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0);

    /* Perform the request, res will get the return code */
    res = curl_easy_perform(curl);
    /* Check for errors */
    if(res != CURLE_OK)
    {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
      return;
    }

    /* always cleanup */
    curl_easy_cleanup(curl);

    *bytes_written = chunk.curr_size;
}
