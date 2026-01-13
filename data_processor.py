"""
Employee Data Processing System
===============================

A comprehensive data processing system demonstrating:
- Advanced data structures (sets, tuples, dictionaries)
- File handling (CSV, JSON, TXT)
- List comprehensions and lambda functions
- Exception handling and logging
- Data transformation and analysis

Author: [Your Name]
Date: January 2026
Portfolio Project: Day 2 - Advanced Python
"""

import json
import csv
from datetime import datetime
from typing import List, Dict, Tuple, Set
from functools import reduce


class DataProcessor:
    """
    Main data processor class handling multiple data formats
    and performing various transformations.
    """
    
    def __init__(self):
        self.employees = []
        self.departments = {}
        self.salary_data = []
        self.errors = []
        
    def load_csv_data(self, filename: str) -> List[Dict]:
        """
        Load employee data from CSV file with error handling.
        
        Args:
            filename (str): Path to CSV file
            
        Returns:
            List[Dict]: List of employee records
        """
        print(f"\n{'='*60}")
        print(f"Loading CSV data from: {filename}")
        print(f"{'='*60}")
        
        employees = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Validate and clean data
                        employee = {
                            'emp_id': row['emp_id'].strip(),
                            'name': row['name'].strip().title(),
                            'department': row['department'].strip().upper(),
                            'salary': float(row['salary']),
                            'joining_date': row['joining_date'].strip(),
                            'email': row['email'].strip().lower()
                        }
                        
                        # Validate email
                        if '@' not in employee['email']:
                            raise ValueError(f"Invalid email: {employee['email']}")
                        
                        # Validate salary
                        if employee['salary'] <= 0:
                            raise ValueError(f"Invalid salary: {employee['salary']}")
                        
                        employees.append(employee)
                        
                    except (ValueError, KeyError) as e:
                        error_msg = f"Row {row_num}: {str(e)}"
                        self.errors.append(error_msg)
                        print(f"⚠️  Warning: {error_msg}")
                        continue
                
            print(f"✅ Successfully loaded {len(employees)} records")
            print(f"⚠️  Errors encountered: {len(self.errors)}")
            
            self.employees = employees
            return employees
            
        except FileNotFoundError:
            print(f"❌ Error: File '{filename}' not found")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return []
    
    def load_json_data(self, filename: str) -> Dict:
        """
        Load department data from JSON file.
        
        Args:
            filename (str): Path to JSON file
            
        Returns:
            Dict: Department information
        """
        print(f"\n{'='*60}")
        print(f"Loading JSON data from: {filename}")
        print(f"{'='*60}")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                departments = json.load(file)
            
            print(f"✅ Successfully loaded {len(departments)} departments")
            self.departments = departments
            return departments
            
        except FileNotFoundError:
            print(f"❌ Error: File '{filename}' not found")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON format: {str(e)}")
            return {}
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return {}
    
    def get_unique_departments(self) -> Set[str]:
        """
        Extract unique departments from employee data using sets.
        
        Returns:
            Set[str]: Unique department names
        """
        return {emp['department'] for emp in self.employees}
    
    def get_employee_tuples(self) -> List[Tuple]:
        """
        Convert employee records to tuples for immutable representation.
        
        Returns:
            List[Tuple]: List of employee tuples
        """
        return [
            (
                emp['emp_id'],
                emp['name'],
                emp['department'],
                emp['salary']
            )
            for emp in self.employees
        ]
    
    def filter_by_salary(self, min_salary: float) -> List[Dict]:
        """
        Filter employees by minimum salary using list comprehension.
        
        Args:
            min_salary (float): Minimum salary threshold
            
        Returns:
            List[Dict]: Filtered employees
        """
        return [
            emp for emp in self.employees 
            if emp['salary'] >= min_salary
        ]
    
    def transform_salaries(self, increment_percent: float) -> List[Dict]:
        """
        Apply salary increment using map and lambda.
        
        Args:
            increment_percent (float): Percentage increment
            
        Returns:
            List[Dict]: Employees with updated salaries
        """
        multiplier = 1 + (increment_percent / 100)
        
        return list(map(
            lambda emp: {
                **emp,
                'salary': round(emp['salary'] * multiplier, 2),
                'increment': f"{increment_percent}%"
            },
            self.employees
        ))
    
    def get_high_earners(self, threshold: float) -> List[Dict]:
        """
        Filter high earners using filter and lambda.
        
        Args:
            threshold (float): Salary threshold
            
        Returns:
            List[Dict]: High earning employees
        """
        return list(filter(
            lambda emp: emp['salary'] > threshold,
            self.employees
        ))
    
    def calculate_total_salary(self) -> float:
        """
        Calculate total salary using reduce.
        
        Returns:
            float: Total salary expense
        """
        return reduce(
            lambda total, emp: total + emp['salary'],
            self.employees,
            0
        )
    
    def sort_employees(self, key: str, reverse: bool = False) -> List[Dict]:
        """
        Sort employees by specified key using lambda.
        
        Args:
            key (str): Key to sort by ('name', 'salary', 'department')
            reverse (bool): Sort in descending order
            
        Returns:
            List[Dict]: Sorted employees
        """
        sort_functions = {
            'name': lambda emp: emp['name'],
            'salary': lambda emp: emp['salary'],
            'department': lambda emp: emp['department']
        }
        
        return sorted(
            self.employees,
            key=sort_functions.get(key, lambda emp: emp['name']),
            reverse=reverse
        )
    
    def group_by_department(self) -> Dict[str, List[Dict]]:
        """
        Group employees by department.
        
        Returns:
            Dict: Employees grouped by department
        """
        grouped = {}
        
        for emp in self.employees:
            dept = emp['department']
            if dept not in grouped:
                grouped[dept] = []
            grouped[dept].append(emp)
        
        return grouped
    
    def calculate_department_stats(self) -> Dict[str, Dict]:
        """
        Calculate statistics per department using comprehensions.
        
        Returns:
            Dict: Department statistics
        """
        grouped = self.group_by_department()
        
        return {
            dept: {
                'count': len(employees),
                'total_salary': sum(emp['salary'] for emp in employees),
                'avg_salary': sum(emp['salary'] for emp in employees) / len(employees),
                'min_salary': min(emp['salary'] for emp in employees),
                'max_salary': max(emp['salary'] for emp in employees)
            }
            for dept, employees in grouped.items()
        }
    
    def find_email_duplicates(self) -> Set[str]:
        """
        Find duplicate email addresses using sets.
        
        Returns:
            Set[str]: Duplicate email addresses
        """
        emails = [emp['email'] for emp in self.employees]
        unique_emails = set(emails)
        
        return {
            email for email in unique_emails 
            if emails.count(email) > 1
        }
    
    def clean_data(self) -> List[Dict]:
        """
        Clean and standardize employee data.
        
        Returns:
            List[Dict]: Cleaned employee records
        """
        print(f"\n{'='*60}")
        print("Data Cleaning Process")
        print(f"{'='*60}")
        
        # Remove duplicates based on emp_id
        seen_ids = set()
        unique_employees = []
        
        for emp in self.employees:
            if emp['emp_id'] not in seen_ids:
                seen_ids.add(emp['emp_id'])
                unique_employees.append(emp)
        
        duplicates_removed = len(self.employees) - len(unique_employees)
        print(f"✅ Removed {duplicates_removed} duplicate employee IDs")
        
        # Standardize data
        cleaned = [
            {
                **emp,
                'name': emp['name'].title(),
                'department': emp['department'].upper(),
                'email': emp['email'].lower(),
                'email_domain': emp['email'].split('@')[1] if '@' in emp['email'] else ''
            }
            for emp in unique_employees
        ]
        
        print(f"✅ Standardized {len(cleaned)} records")
        
        self.employees = cleaned
        return cleaned
    
    def generate_report(self, output_file: str) -> None:
        """
        Generate comprehensive text report.
        
        Args:
            output_file (str): Path to output file
        """
        print(f"\n{'='*60}")
        print("Generating Report")
        print(f"{'='*60}")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                # Header
                file.write("="*80 + "\n")
                file.write("EMPLOYEE DATA ANALYSIS REPORT\n")
                file.write("="*80 + "\n")
                file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Total Employees: {len(self.employees)}\n\n")
                
                # Summary Statistics
                file.write("SUMMARY STATISTICS\n")
                file.write("-"*80 + "\n")
                total_salary = self.calculate_total_salary()
                avg_salary = total_salary / len(self.employees) if self.employees else 0
                
                file.write(f"Total Salary Expense: ${total_salary:,.2f}\n")
                file.write(f"Average Salary: ${avg_salary:,.2f}\n")
                file.write(f"Unique Departments: {len(self.get_unique_departments())}\n\n")
                
                # Department Statistics
                file.write("DEPARTMENT BREAKDOWN\n")
                file.write("-"*80 + "\n")
                dept_stats = self.calculate_department_stats()
                
                for dept, stats in sorted(dept_stats.items()):
                    file.write(f"\n{dept}:\n")
                    file.write(f"  Employees: {stats['count']}\n")
                    file.write(f"  Total Salary: ${stats['total_salary']:,.2f}\n")
                    file.write(f"  Average Salary: ${stats['avg_salary']:,.2f}\n")
                    file.write(f"  Salary Range: ${stats['min_salary']:,.2f} - ${stats['max_salary']:,.2f}\n")
                
                # Top Earners
                file.write("\n" + "="*80 + "\n")
                file.write("TOP 10 EARNERS\n")
                file.write("-"*80 + "\n")
                top_earners = self.sort_employees('salary', reverse=True)[:10]
                
                for rank, emp in enumerate(top_earners, 1):
                    file.write(f"{rank:2d}. {emp['name']:30s} {emp['department']:15s} ${emp['salary']:>10,.2f}\n")
                
                # Data Quality Issues
                if self.errors:
                    file.write("\n" + "="*80 + "\n")
                    file.write("DATA QUALITY ISSUES\n")
                    file.write("-"*80 + "\n")
                    for error in self.errors:
                        file.write(f"• {error}\n")
                
                file.write("\n" + "="*80 + "\n")
                file.write("END OF REPORT\n")
                file.write("="*80 + "\n")
            
            print(f"✅ Report saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error generating report: {str(e)}")
    
    def export_to_json(self, output_file: str) -> None:
        """
        Export cleaned data to JSON format.
        
        Args:
            output_file (str): Path to output JSON file
        """
        print(f"\n{'='*60}")
        print("Exporting to JSON")
        print(f"{'='*60}")
        
        try:
            export_data = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'total_records': len(self.employees),
                    'departments': list(self.get_unique_departments())
                },
                'employees': self.employees,
                'statistics': self.calculate_department_stats()
            }
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(export_data, file, indent=4, ensure_ascii=False)
            
            print(f"✅ Data exported to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error exporting JSON: {str(e)}")
    
    def export_to_csv(self, output_file: str) -> None:
        """
        Export processed data to CSV format.
        
        Args:
            output_file (str): Path to output CSV file
        """
        print(f"\n{'='*60}")
        print("Exporting to CSV")
        print(f"{'='*60}")
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                if not self.employees:
                    print("⚠️  No data to export")
                    return
                
                fieldnames = self.employees[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(self.employees)
            
            print(f"✅ Data exported to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error exporting CSV: {str(e)}")


def main():
    """
    Main execution function demonstrating all features.
    """
    print("="*80)
    print("EMPLOYEE DATA PROCESSING SYSTEM")
    print("Demonstrating Advanced Python Concepts")
    print("="*80)
    
    # Initialize processor
    processor = DataProcessor()
    
    # Load data from CSV
    processor.load_csv_data('employees.csv')
    
    # Load department data from JSON
    processor.load_json_data('departments.json')
    
    # Clean data
    processor.clean_data()
    
    # Demonstrate set operations
    print(f"\n{'='*60}")
    print("Unique Departments (Using Sets)")
    print(f"{'='*60}")
    unique_depts = processor.get_unique_departments()
    print(f"Departments: {', '.join(sorted(unique_depts))}")
    
    # Demonstrate tuple usage
    print(f"\n{'='*60}")
    print("Employee Records as Tuples")
    print(f"{'='*60}")
    employee_tuples = processor.get_employee_tuples()
    for emp_tuple in employee_tuples[:5]:
        emp_id, name, dept, salary = emp_tuple
        print(f"{emp_id}: {name:20s} {dept:15s} ${salary:>10,.2f}")
    
    # Demonstrate list comprehension
    print(f"\n{'='*60}")
    print("High Earners (Salary > $70,000)")
    print(f"{'='*60}")
    high_earners = processor.filter_by_salary(70000)
    print(f"Found {len(high_earners)} high earners")
    
    # Demonstrate lambda with map
    print(f"\n{'='*60}")
    print("Salary Projection (10% Increment)")
    print(f"{'='*60}")
    projected = processor.transform_salaries(10)
    for emp in projected[:5]:
        print(f"{emp['name']:25s} ${emp['salary']:>10,.2f} (+{emp['increment']})")
    
    # Demonstrate lambda with filter
    print(f"\n{'='*60}")
    print("Department Statistics")
    print(f"{'='*60}")
    dept_stats = processor.calculate_department_stats()
    for dept, stats in sorted(dept_stats.items()):
        print(f"\n{dept}:")
        print(f"  Employees: {stats['count']}")
        print(f"  Avg Salary: ${stats['avg_salary']:,.2f}")
    
    # Demonstrate reduce
    print(f"\n{'='*60}")
    print("Total Salary Calculation (Using Reduce)")
    print(f"{'='*60}")
    total_salary = processor.calculate_total_salary()
    print(f"Total Company Salary Expense: ${total_salary:,.2f}")
    
    # Generate outputs
    processor.generate_report('output/employee_report.txt')
    processor.export_to_json('output/processed_data.json')
    processor.export_to_csv('output/cleaned_employees.csv')
    
    print("\n" + "="*80)
    print("✅ PROCESSING COMPLETE!")
    print("="*80)
    print("\nGenerated Files:")
    print("  • output/employee_report.txt")
    print("  • output/processed_data.json")
    print("  • output/cleaned_employees.csv")
    print("="*80)


if __name__ == "__main__":
    main()
