## ToDo list status:

The code for this assignment needs to meet the following items to meet a perfect score.

🚧 Include this emoji if currently working on it to avoid overlap

| **Function**  | **Points**  | **Break down**  | **Item**  | **Yassine J**  |  **Samuel A** |
|---------------|-------------|-----------------|-----------|----------------|---------------|
|   **Input**   |  1 |  1 | No usage info if incorrect args  |               |               |
|  **Request**  |  3 |  1<br />1<br />1<br />| Correct GET syntax<br />Hostname in rqst<br />User agent in rqst<br />|   |    |
|**Receive loop**| 4  | 1<br />2<br />1<br />  |  Dynamic buffer resizing<br /> Fails to receive/parse 96MB file<br /> Select()<br />  |   |   |
|  **Output**  | 10  | 3<br />1<br />1<br />1<br />1<br />1<br />1<br />1<br />  | Correct host/port/rqst<br />Correct DNS info<br />Timing of connect()<br />Timing of recv()<br />Correct page size<br />Correct HTTP status<br />Correct number of links<br />Correct HTTP header shown<br />   | :heavy_check_mark:<br />:heavy_check_mark:<br />:heavy_check_mark:<br />:heavy_check_mark:<br /><br /><br /><br /><br />  |<br /><br /><br /><br /><br /><br /><br /><br /> |
|  **Errors**  | 6  | 1<br />1<br />1<br />1<br />1<br />1<br />  | Handle invalid port/scheme<br />Notify of DNS failure<br />Notify of connect failure<br />Notify of recv() failure<br />Notify of non-HTTP reply <br />Parses non-2xx pages<br />  |   |    |
|  **Other**  | 1  | 1  | Missing files for compilation  |   |   |



## Current Code Output:

![Output](/figures/current_out.png)

![Fail Output](/figures/fail_output.png)

## Goal of this part 1 of the assignment:

![Goal](/figures/goal.png)
