import train
import pretrain_STREAM
import sys

print("Which do you want to run ?")
print("train: 1, pretrain: 2")
x = input()

print("BRANCH_NUM ?: ", end="")
branch_num = int(input())
print("MAX_EPOCH ?: ", end="")
max_epoch = int(input())

if x == "1":
    train.main(branch_num, max_epoch)
elif x == "2":
    pretrain_STREAM.main(branch_num, max_epoch)
else:
    print("Please select 1 or 2")
    sys.exit()


def get_branch_num():
    return branch_num


def get_max_epoch():
    return max_epoch

