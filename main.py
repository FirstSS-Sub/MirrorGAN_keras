import train
import pretrain_STREAM
import sys

print("Which do you want to run ?")
print("train: 1, pretrain: 2")
x = input()

if x == "1":
    train.main()
elif x == "2":
    pretrain_STREAM.main()
else:
    print("Please select 1 or 2")
    sys.exit()
