drop database project;
create database project;
use project;
create table officer_record(
  officer_id int primary key,
  name varchar(40),
  address varchar(100),
  age int,
  gender varchar(15),
  phone int,
  email_id varchar(30),
  qualification varchar(40),
  aadhar int
);
create table police_station(
  ps_id int primary key,
  ps_name varchar(40),
  address varchar(100),
  phone int,
  officer_id int,
  foreign key (officer_id) references officer_record(officer_id)
);
create table complainer(
  complainer_id int primary key,
  name varchar(40),
  address varchar(100),
  age int,
  gender varchar(15),
  phone int,
  aadhar int
);
create table crime_register(
  crime_id int primary key,
  date_of_offence date,
  fir_no int,
  ps_id int,
  date_of_report date,
  case_status varchar(20),
  arrested varchar(15),
  challan_id int,
  officer_id varchar(15),
  case_description varchar(50),
  accused_id int,
  complainer_id int,
  foreign key (ps_id) references police_station(ps_id),
  foreign key (complainer_id) references complainer(complainer_id)
);
create table witness(
  witness_id int primary key,
  name varchar(40),
  address varchar(100),
  age int,
  gender varchar(15),
  phone int,
  aadhar int
);
create table accused(
  accused_id int primary key,
  name varchar(40),
  address varchar(100),
  age int,
  gender varchar(15),
  phone int,
  aadhar int
);
create table section(
  section_id int primary key,
  section_description varchar(50)
);
create table victim(
  victim_id int primary key,
  name varchar(40),
  address varchar(100),
  age int,
  gender varchar(15),
  phone int,
  aadhar int
);