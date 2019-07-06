package main

import (
	"fmt"
	"os"
	"bufio"
	"sync"
	"strings"
)

func main() {
	fmt.Println("[Running...]")

	file, err := os.Open("out.txt")
	if err != nil {
		fmt.Printf("[Error]: %s\n", err)
	}
	defer file.Close()

	store := Storage{
		Map: make(map[int]Event),
		Lock: new(sync.Mutex),
	}
	var wg sync.WaitGroup

	counter := 0
	scanner := bufio.NewScanner(file)
	
	for scanner.Scan() {
		counter += 1
		wg.Add(1)

		go func(id int, text string) {
			defer wg.Done()

			if strings.HasPrefix(text, "[") {
				newEvent := Factory(text)
				
				store.Lock.Lock()
				store.Map[id] = newEvent
				store.Lock.Unlock()
			}
		}(counter, scanner.Text())
	}

	wg.Wait()
	fmt.Println("[Analysing...]", counter)

// Now obey the MIT TypeB protocol...

	collection := Collection{
		Slots: make([]Slot, 5),
	}
	slotNow := 0
	collection.Slots[0] = Slot {
		Tracks: []Track{},
		Used: true,
	}
	var trackNow Track
	posNow := make([]Position, 5)
	widthNow := make([]int64, 5)
	trackCounter := 0
	for i:=1; i<=counter; i++ {
		eventNow := store.Map[i]

        if eventNow.Statu == "EV_ABS" {
        	if eventNow.Info == "ABS_MT_TRACKING_ID" {
        		if eventNow.Value == -1 {
        			if i<counter && store.Map[i+1].Statu == "EV_KEY" {
        				// the up action
        				trackNow.Reports = append(trackNow.Reports, Report {
        					Time: store.Map[i+1].Time,
        					IsBtn: true,
        				})

        				collection.Slots[slotNow].Tracks = append(collection.Slots[slotNow].Tracks, trackNow)
        				trackNow = Track{}
        				// fmt.Println("Track is done.")
        			}

        			collection.Slots[slotNow].Tracks = append(collection.Slots[slotNow].Tracks, trackNow)
        			// close the slot here
        			posNow[slotNow] = Position{}
        			widthNow[slotNow] = 0
        			trackCounter += 1
        		} else {
        			trackNow = Track{
        				ID: eventNow.Value,
        				Reports: []Report{},
        			}
        		}
        	} else if eventNow.Info == "ABS_MT_SLOT" {
        		// update the slot
        		if int64(slotNow) != eventNow.Value {
        			slotNow = int(eventNow.Value)
        		}

        		// init new slot
        		if !collection.Slots[slotNow].Used {
        			collection.Slots[slotNow] = Slot {
        				Used: true,
        				Tracks: []Track{},
        			}
        		}
        	} else if eventNow.Info == "ABS_MT_POSITION_X" {
        		posNow[slotNow].X = eventNow.Value
        	} else if eventNow.Info == "ABS_MT_POSITION_Y" {
        		posNow[slotNow].Y = eventNow.Value
        	} else if eventNow.Info == "ABS_MT_WIDTH_MAJOR" {
        		widthNow[slotNow] = eventNow.Value
        	}
        } else { // EV_SYN
        	if i > 1 && strings.HasPrefix(store.Map[i-1].Info, "ABS_MT_POSITION_") {
        		// report the position
        		trackNow.Reports = append(trackNow.Reports, Report {
        			Time: store.Map[i-1].Time,
        			IsBtn: false,
        			Pos: Position {
        				X: posNow[slotNow].X,
        				Y: posNow[slotNow].Y,
        			},
        			Width: widthNow[slotNow],
        		})
        		// fmt.Println("New Position:", posNow[slotNow])
        	}
        }
	}
	fmt.Printf("[Over...]: Have %d tracks.\n", trackCounter)
	return
}