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


// Load day x input into vector of lines.
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

// Load <repo>/inputs/<filename> into vector of lines.
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

// Given vector of lines, make a map with key: (x, y) coords and value: char
// key: std::pair<int64_t, int64_t>
// value: char
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

// Given vector of lines, make a map with key: (x, y) coords and value: map_char_to_T(input char)
// key: std::pair<int64_t, int64_t>
// value: T = F(char)
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

// Find first key with a particular value in map m, or None
template <typename M, typename V, typename K=typename M::key_type>
std::optional<K> map_find_first_value(M m, V value)
{
    for (auto const& [k, v] : m)
    {
        if (v == value)
        {
            return std::optional<K>{k};
        }
    }
    return {};
}

// Find all keys with a particular value in map m
template <typename M, typename V, typename K=typename M::key_type>
std::vector<K> map_find_value(M m, V value)
{
    std::vector<K> output;
    for (auto const& [k, v] : m)
    {
        if (v == value)
        {
            output.push_back(k);
        }
    }
    return output;
}

struct Point2D {
    Point2D(std::pair<int64_t, int64_t> p) : x(p.first), y(p.second) {};
    Point2D(int64_t px, int64_t py) : x(px), y(py) {};
    int64_t x, y;

    friend std::ostream& operator<<(std::ostream& stream, const Point2D& p) {
        return stream << "(" << p.x << ", " << p.y << ")";
    }
};

bool operator==(Point2D lhs, Point2D rhs) {
    if (lhs.x == rhs.x && lhs.y == rhs.y) {
        return true;
    } else {
        return false;
    }
}

// Impl Hash on Point2D
template<>
struct std::hash<Point2D> {
    size_t operator()(const Point2D& point) const noexcept
    {
        size_t xhash = std::hash<int64_t>{}(point.x);
        size_t yhash = std::hash<int64_t>{}(point.y);
        return xhash ^ (yhash << 1);
    }
};

// Impl Hash on std::pair because it's not already there for some reason
template <typename T1, typename T2>
struct std::hash<std::pair<T1, T2>> {
    size_t operator()(const std::pair<T1, T2> &p) const noexcept {
        return std::hash<T1>{}(p.first) ^ (std::hash<T2>{}(p.second) << 1);
    }
};

const Point2D north = Point2D { 0, -1 };
const Point2D east = Point2D { 1, 0 };
const Point2D south = Point2D { 0, 1 };
const Point2D west = Point2D { -1, 0 };

Point2D operator+(Point2D lhs, Point2D rhs) {
    return Point2D { lhs.x + rhs.x, lhs.y + rhs.y };
}

Point2D operator-(Point2D lhs, Point2D rhs) {
    return Point2D { lhs.x - rhs.x, lhs.y - rhs.y };
}

Point2D operator*(Point2D lhs, Point2D rhs) {
    return Point2D { lhs.x * rhs.x, lhs.y * rhs.y };
}

Point2D operator/(Point2D lhs, Point2D rhs) {
    return Point2D { lhs.x / rhs.x, lhs.y / rhs.y };
}

void examples() {
    auto lines1= load(6);
    auto lines2 = load("06a.txt");
    auto map2 = make_map(lines1); // overloaded case uses default lambda: [](char c) -> char { return c; }
    auto map3 = make_map(lines1, [](char c) -> uint64_t {
            switch (c) {
                case '^': return 2;
                case '#': return 1;
                case '.': return 0;
                default: return 0;
            };
        });
    auto guard = map_find_first_value(map2, '^').value(); // throws if no '^' in map2
    auto walls = map_find_value(map2, '#'); // gets std::vector<key> of keys with value '#'
}
