#include <iostream>

int main(void) {
    char * f_n = "jon ";
    char * l_n = "shidal";
    int a = 100;
    int *pa = &a;
    //f_n += l_n;
    std::cout << f_n << l_n << std::endl;
    std::cout << (void *)f_n << " "<< (void*)l_n << std::endl;
    std::cout << "a is " << a << std::endl;
    std::cout << "a address pa is " << pa << std::endl;
    std::cout << "pa points to value " << *pa << std::endl;

}
