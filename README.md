# DATABASE_FINAL

## I. Install
    cd DATABASE_FINAL
    pip install -r requirement.txt

## II. Usage
1. Run the following SQL scripts to create the corresponding databases:
   - Run `sql/CreateSchema1.sql` to create the first database schema.
   - Run `sql/CreateSchema2.sql` to create the second database schema.

2. Run the `generate_db.py` file to generate data and insert it into the database:
       
       ython generate_db.py --u user --n dbname --p password

3. Run the `querry.py` file to perform queries and measure execution time:
   
        python querry.py --n1 TRUONGHOC1 --n2 TRUONGHOC2 --sn schoolname --y years --t type --c querry_choice
        
The results, including execution time and an XML file, will be outputted immediately.
  
4. Run the `querry_xml.py` file to query the XML file:

        python querry_xml.py --f xml_file --s thres_start --e thres_end
        
Please note that you need to replace some variable behind the parser such as `user`, `dbname`, `password`, ... with your own credentials. Also, make sure to provide the appropriate values for the command-line arguments specified in the usage instructions.

If you have any questions, feel free to reach out.
