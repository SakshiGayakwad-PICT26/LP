#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;

// Function to display page frames and miss status
void displayFrames(const vector<int>& frames, bool isHit, int page) {
    if (isHit) {
        cout << "Page Hit: " << page << " - Frame: ";
    } else {
        cout << "Page Miss: " << page << " - Frame: ";
    }
    for (int f : frames) {
        cout << f << " ";
    }
    cout << endl;
}

// FIFO Page Replacement
void FIFO(const vector<int>& pages, int capacity) {
    vector<int> frames;
    int pageFaults = 0, hits = 0;

    for (int page : pages) {
        bool isHit = (find(frames.begin(), frames.end(), page) != frames.end());
        if (!isHit) {
            if (frames.size() == capacity) {
                frames.erase(frames.begin());
            }
            frames.push_back(page);
            pageFaults++;
        } else {
            hits++;
        }
        displayFrames(frames, isHit, page);
    }
    cout << "Hits: " << hits << endl;
    cout << "Misses: " << pageFaults << endl;
    cout << "Hit Ratio: " << static_cast<double>(hits) / pages.size() << endl;
}

// LRU Page Replacement
void LRU(const vector<int>& pages, int capacity) {
    vector<int> frames;
    unordered_map<int, int> lru_map; // Stores the last used time of each page
    int pageFaults = 0, hits = 0;
    int time = 0;

    for (int page : pages) {
        bool isHit = (find(frames.begin(), frames.end(), page) != frames.end());
        if (!isHit) {
            if (frames.size() == capacity) {
                // Find LRU page
                int lru = frames[0];
                for (int f : frames) {
                    if (lru_map[f] < lru_map[lru]) {
                        lru = f;
                    }
                }
                frames.erase(remove(frames.begin(), frames.end(), lru), frames.end());
            }
            frames.push_back(page);
            pageFaults++;
        } else {
            hits++;
        }
        lru_map[page] = time++;
        displayFrames(frames, isHit, page);
    }
    cout << "Hits: " << hits << endl;
    cout << "Misses: " << pageFaults << endl;
    cout << "Hit Ratio: " << static_cast<double>(hits) / pages.size() << endl;
}

// Optimal Page Replacement
void Optimal(const vector<int>& pages, int capacity) {
    vector<int> frames;
    int pageFaults = 0, hits = 0;

    for (int i = 0; i < pages.size(); ++i) {
        int page = pages[i];
        bool isHit = (find(frames.begin(), frames.end(), page) != frames.end());
        if (!isHit) {
            if (frames.size() == capacity) {
                int farthest = i, replaceIdx = -1;
                for (int j = 0; j < frames.size(); ++j) {
                    auto pos = find(pages.begin() + i + 1, pages.end(), frames[j]);
                    int distance = (pos == pages.end()) ? pages.size() : pos - pages.begin();
                    if (distance > farthest) {
                        farthest = distance;
                        replaceIdx = j;
                    }
                }
                if (replaceIdx == -1) replaceIdx = 0;
                frames[replaceIdx] = page;
            } else {
                frames.push_back(page);
            }
            pageFaults++;
        } else {
            hits++;
        }
        displayFrames(frames, isHit, page);
    }
    cout << "Hits: " << hits << endl;
    cout << "Misses: " << pageFaults << endl;
    cout << "Hit Ratio: " << static_cast<double>(hits) / pages.size() << endl;
}

int main() {
    int capacity, choice;
    cout << "Enter number of frames: ";
    cin >> capacity;

    int n;
    cout << "Enter number of pages: ";
    cin >> n;

    vector<int> pages(n);
    cout << "Enter page references:\n";
    for (int i = 0; i < n; ++i) {
        cin >> pages[i];
    }

    cout << "Enter algorithm choice:\n1. FIFO\n2. LRU\n3. Optimal\nEnter choice: ";
    cin >> choice;

    switch (choice) {
        case 1:
            FIFO(pages, capacity);
            break;
        case 2:
            LRU(pages, capacity);
            break;
        case 3:
            Optimal(pages, capacity);
            break;
        default:
            cout << "Invalid choice!" << endl;
    }

    return 0;
}