#include <gtest/gtest.h>
#include "calculator.h"

TEST(CalculatorTest, AddNumbers)
{
EXPECT_EQ(add_numbers(2,3),5);
EXPECT_EQ(add_numbers(-1,0.5),-0.5);
}

TEST(CalculatorTest, SubtractNumbers)
{
EXPECT_EQ(sub_numbers(4,2),2);
EXPECT_EQ(sub_numbers(-1,2),-3);
}

int main(int argc, char **argv)
{
testing::InitGoogleTest(&argc, argv);
return RUN_ALL_TESTS();
}
