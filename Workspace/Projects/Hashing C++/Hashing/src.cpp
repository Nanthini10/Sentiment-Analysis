#include<fcntl.h>
#define LEN 40
#define N 5
#include<iostream>
#include<sys/types.h>
#include<stdio.h>
#include<fstream>
#include<sys/stat.h>
#include<stdlib.h>
using namespace std;
class student
{
    char name[25],usn[11],age[4],str[LEN];
    int fd;
    unsigned int hash(char*);
    void pack();
    void unpack();
    public:
    student();
    ~student();
    void add();
    void search();
};

//Constructor  
student::student()
{
    if( ( fd=open("./student",O_RDWR) ) == -1)
    {
           char buf[(LEN+1)*N];
           int i;
           for(i=0;i<(LEN+1)*N;i++) // initialize the buffer or hash table
           	buf[i]='/';
           fd=open("./student",O_RDWR|O_CREAT|O_EXCL,0666);
           write(fd,buf,(LEN+1)*N);  //open a file and write the buffer
    }
}

void student::pack()
{
    strcpy(str,usn);
    strcat(str,"|");
    strcat(str,name);
    strcat(str,"|");
    strcat(str,age);
    for(int i=strlen(str);i<LEN-1;i++)
       strcat(str,"#");  
}
void student::unpack()
{
    strcpy(usn,strtok(str,"|"));
    strcpy(name,strtok(NULL,"|"));
    strcpy(age,strtok(NULL,"#"));
}
unsigned int student::hash(char *str)
{
    //djb2 algorithm to calculate the hash address
    unsigned int hash = 0;
    int c;
    while (c = *str++)
           hash=hash*33+c;
    return hash % N;
}

// add one record to hash table using hash function mentioned above
void student::add()
{
    int home_address,i=0;
    char test;
    char test_buf[2];
    cout<<"Enter USN: ";
    cin>>usn;
    cout<<"Enter name: ";
    cin>>name;
    cout<<"Enter age: ";
    cin>>age;
    pack( );
    home_address=hash(name);
    while(1)
    {
           if(i==N)
           {
               cout<<"Overflow!\n"; // hash table doesn’t have space
               return;
           }
           lseek(fd,(LEN+1)*home_address,SEEK_SET);
           read(fd,&test,sizeof(test));
           if(test=='/')  //hash address is free or  no collision
               break;
           
          home_address=(home_address+1)%N;
           i++;
    }
    lseek(fd,(LEN+1)*home_address,SEEK_SET);
    write(fd,str,LEN);
    write(fd,"\n",1);
}

//function to search for a record using hash function
void student::search()
{
    char key[25];
    int home_address,i=0;
    cout<<"Enter key: ";
    cin>>key;
    home_address=hash(key);
    do
    {
           lseek(fd,(LEN+1)*home_address,SEEK_SET);
           read(fd,str,LEN);
           unpack();
           home_address=(home_address+1)%N;
           i++;
    }while(strcmp(name,key) && i<N);
    if(strcmp(name,key))
           cout<<"Not found!\n";
    else
    {
           cout<<"Student found\n";
           cout<<"Name = "<<name;
           cout<<"\nUSN = "<<usn;
           cout<<"\nAge = "<<age<<endl;
    }
}
student::~student()
{
    close(fd);
}
int main()
{
    int ch;
    student s;
    do
    {
           cout<<"\n1. Add\n2. Search\n3. Exit\n\nEnter choice: ";
           cin>>ch;
           switch(ch)
           {
           case 1:
               s.add();
               break;
           case 2:
               s.search();
               break;
           case 3:
               break;
           default:
               cout<<"Wrong choice!";
           }
    }while(ch!=3);
}
