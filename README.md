# py-workday

Generates working days for you.
Needs a little cleaning up as well as more information for other public holidays than just Finland.


Example:
```python
wd = Workdays(
    dt_from=datetime.datetime(2021, 1, 1),
    dt_to=datetime.datetime(2021, 12, 31)
)
print(len(wd.workdays))
```