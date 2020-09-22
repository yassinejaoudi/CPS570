## Team Members:
* Yassine Jaoudi
* Akpan, Samuel Cyril
* Samantha Clark

## Usage:

Use the following command to run the code:

```bash
python Asg1CrawlThread.py 1 URL-input-100.txt
```

The code accepts two arguments, first one indicates the number of threads to run and the second one the input file

## ToDo list status:

The code for this assignment needs to meet the following items to meet a perfect score.

* :construction: Include this emoji if you choose to work on the appropriate task
* :recycle: Include if this task is done, but it needs to be rechecked by another teammate
* :heavy_check_mark: Include this one if its done


:rotating_light::rotating_light::rotating_light: Choose 4 or 5 tasks within the output and logic function as the other functions are either already implemented or are a quick fix just to split the work fairly.

| **Function**  | **Points**  | **Break down**  | **Item**  | **Samantha** | **Samuel** | **Yassine** | 
|---------------|-------------|-----------------|-----------|--------------|------------|-------------|
|  **Running Output**  | 12  | 1<br />1<br />1<br />1<br />1<br />1<br />1<br />1<br />1<br />1<br />1<br />1<br />  | Printouts every 2 seconds<br />Correct active threads<br />Correct queue size<br />Correct extracted URLs<br />Correct unique hosts<br />Correct DNS lookups<br />Correct Unique IPs()<br />Correct attempted robots<br />Correct crawled URLs<br />Correct parsed links<br />Correct pps<br />  Correct Mbps<br />   | <br /> <br /> <br /> <br /><br /><br /><br /><br /><br /><br /> | <br /><br /><br /><br /><br /> <br /> <br /><br /> <br /><br />| <br /><br /><br /><br /> <br /><br /><br /><br /><br /> <br /> |
|  **Summary**  | 6  | 1<br />1<br />1<br />1<br />1<br />1<br />  | Correct URL processing rate<br />Correct DNS rate<br />Correct robots rate<br />Correct crawled rate/totals<br />Correct parser speed <br />Correct HTTP breakdown <br />  | <br /> <br /><br /><br /> | <br /><br /><br /><br />  |  <br /><br /> <br /> <br /> |
|**Code**| 6  | 1<br />1<br />2<br />1<br />1<br />  |  >>20Mbps w/ 500 threads <br /> >>200MB RAM w/500 threads<br /> No deadlocks on exit<br />No issues with the file reader <br /> No improper stats thread<br />  | <br /><br /><br /><br /><br />  | <br /><br /><br /><br /><br /> |  <br /><br /> <br /><br /><br /> |
|  **Other**  | 1  | 1  | No Missing files for compilation  |  |   | :heavy_check_mark:  |
|  **Report**  | 25  | 5<br />5<br />5<br />5<br />5<br />  | Lessons learned and trace<br />Google graph-size analyis<br />Yahoo band-width analysis<br /> Probability analysis<br /> Written Report<br />  |  |   |  |

## :bug: Bug Fixes :bug: :

| **Bug** | **Status** | **Fix Implemented** | **Fixed by** |
|---------|------------|---------------------|--------------|
| While loop stuck on the first recieved Q element |  Fixed :heavy_check_mark: | Inside the if statement, there was a need of releasing the lock after crawling function which was missing | **YJ** |
| No excpetion error for checking robots fct |  Fixed :heavy_check_mark: | Fixed by adding an expetion handling  | **SCA** |


## Code Output:
![output](current_out_part2.png)

## Goal of this part 2 of the assignment:

![Goal](part2_goal_output.png)

## Tasks done from previous assignment part:

* Correct page size
* Correct number of links

## :sparkles: Future Work :sparkles:

* Find a way to specify the buffer size dynamically.
* Current code runtime is **118.58 ms**, we will be improving this runtime by making the code more effecient in order to decrease the runtime.
* Improve the overall design of the code. 
