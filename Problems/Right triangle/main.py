class RightTriangle:
    def __init__(self, hyp, leg_1, leg_2):
        self.c = hyp
        self.a = leg_1
        self.b = leg_2
        # calculate the area here
        if pow(self.c, 2) != pow(self.a, 2) + pow(self.b, 2):
            self.area = "Not right"
        else:
            self.area = 0.5 * self.a * self.b


# triangle from the input
input_c, input_a, input_b = [int(x) for x in input().split()]

# write your code here
triangle = RightTriangle(input_c, input_a, input_b)

print(triangle.area)
