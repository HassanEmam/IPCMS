database=`mysql --user=root --password='' -e "SHOW DATABASES"`
for db in $database; do
    echo "$db"
    mysqldump --user="root" --password='' --databases "$db" > ./"$db".sql
    gzip "$db"
done
