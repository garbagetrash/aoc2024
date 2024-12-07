#pragma once

#include <cstdint>
#include <exception>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <map>
#include <sstream>
#include <string>
#include <type_traits>
#include <utility>
#include <vector>

std::vector<std::string> load(uint64_t day)
{
    std::stringstream daystr;
    daystr << std::setw(2) << std::setfill('0') << day;
    std::string path = std::string(base_dir) + "/inputs/" + daystr.str() + ".txt";
    std::ifstream file(path);
    if (!file.is_open()) {
        throw std::runtime_error("failed to open file: " + path);
    }

    std::vector<std::string> output;
    std::istream_iterator<std::string> it(file);
    std::istream_iterator<std::string> end;
    while (it != end)
    {
        output.push_back(*it++);
    }
    file.close();

    return output;
}

std::vector<std::string> load(std::string filename)
{
    std::string path = std::string(base_dir) + "/inputs/" + filename;
    std::ifstream file(path);
    if (!file.is_open()) {
        throw std::runtime_error("failed to open file: " + path);
    }

    std::vector<std::string> output;
    std::istream_iterator<std::string> it(file);
    std::istream_iterator<std::string> end;
    while (it != end)
    {
        output.push_back(*it++);
    }
    file.close();

    return output;
}

template <typename T>
class Map2D {
public:
    template <typename F>
    Map2D(std::vector<std::string> lines, F&& map_char_to_T) {
        for (int64_t y = 0; y < lines.size(); y++) {
            for (int64_t x = 0; x < lines[y].size(); x++) {
                m_map.insert({std::make_pair(x, y), map_char_to_T(lines[y][x])});
            }
        }
    };

    std::map<std::pair<int64_t, int64_t>, T> m_map = {};
};

std::map<std::pair<int64_t, int64_t>, char> make_map(std::vector<std::string> lines)
{
    std::map<std::pair<int64_t, int64_t>, char> output = {};
    for (int64_t y = 0; y < lines.size(); y++) {
        for (int64_t x = 0; x < lines[y].size(); x++) {
            output.insert({std::make_pair(x, y), lines[y][x]});
        }
    }

    return output;
};

template <typename F, typename T=decltype(std::declval<F>()(std::declval<char>()))>
std::map<std::pair<int64_t, int64_t>, T> make_map(std::vector<std::string> lines, F&& map_char_to_T)
{
    std::map<std::pair<int64_t, int64_t>, decltype(std::declval<F>()(std::declval<char>()))>
      output = {};
    for (int64_t y = 0; y < lines.size(); y++) {
        for (int64_t x = 0; x < lines[y].size(); x++) {
            output.insert({std::make_pair(x, y), map_char_to_T(lines[y][x])});
        }
    }

    return output;
};

int solve06() {
    //auto input = load(6);
    auto lines = load("06a.txt");
    auto map1 = Map2D<char>(lines, [](char c) { return c; });
    auto map2 = make_map(lines);
    auto map3 = make_map(lines, [](char c) -> char { return c; });

    return 0;
}
