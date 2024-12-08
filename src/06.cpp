#include <atomic>
#include <cstdint>
#include <optional>
#include <thread>
#include <unordered_set>
#include <vector>

#include "helpers.h"

Point2D rotate_right(Point2D p)
{
    if (p == north) {
        return east;
    } else if (p == east) {
        return south;
    } else if (p == south) {
        return west;
    } else if (p == west) {
        return north;
    } else {
        return north;
    }
}

template <typename M>
std::pair<size_t, bool> simulate(M m, Point2D guardpos, Point2D guarddir)
{
    std::unordered_set<std::pair<Point2D, Point2D>> states;
    std::unordered_set<Point2D> visited;
    visited.insert(guardpos);
    bool infbool = false;
    while (true)
    {
        auto nextpos = guardpos + guarddir;
        //std::cout << nextpos << std::endl;
        auto nextkey = std::make_pair(nextpos.x, nextpos.y);
        if (m.count(nextkey) > 0) {
            // Still in area
            if (m[nextkey] == '#') {
                // Hit wall
                guarddir = rotate_right(guarddir);
            } else {
                // Walk
                guardpos = nextpos;
                visited.insert(guardpos);
            }
            auto newstate = std::make_pair(guardpos, guarddir);
            if (states.count(newstate) > 0) {
                // Encountered this state before, infinite loop! bail.
                infbool = true;
                break;
            } else {
                // New state, keep track of it
                states.insert(newstate);
            }
        } else {
            // Walked out of area
            break;
        }
    }
    return std::make_pair(visited.size(), infbool);
}

int main()
{
    auto lines = load("06a.txt");
    auto m = make_map(lines);

    auto guard = map_find_first_value(m, '^').value();
    auto walls = map_find_value(m, '#');
    auto guarddir = north;

    // Part 1
    auto [visited, infbool] = simulate(m, Point2D(guard), guarddir);
    std::cout << "# visited: " << visited << std::endl;
    
    // Part 2
    int64_t xmax = 130;
    int64_t ymax = 130;
    std::atomic<size_t> cntr{0};
    std::vector<std::thread> thread_handles;
    for (int64_t x = 0; x < xmax; x++)
    {
        for (int64_t y = 0; y < ymax; y++)
        {
            thread_handles.push_back(std::thread([m, x, y, guard, guarddir, &cntr]() {
                auto mm = m;
                mm.insert({std::make_pair(x, y), '#'});
                auto [visited, infbool] = simulate(mm, Point2D(guard), guarddir);
                if (infbool) {
                    std::cout << "asdf" << std::endl;
                    cntr++;
                }
            }));
        }
    }

    for (auto &t : thread_handles) {
        t.join();
    }
    std::cout << "# inf loops: " << cntr << std::endl;

    return 0;
}
