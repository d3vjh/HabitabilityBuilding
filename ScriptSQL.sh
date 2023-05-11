#!/bin/bash




# Para la Tabla Apartment
for i in {101..701..100}; do echo "INSERT INTO apartment(k_apartment, q_air_humidity, q_ambient_air_humidity, s_apartment_material, q_number_of_bedrooms, q_number_of_occupants, b_is_habitable, k_building) VALUES ($i, 0, 0, 'Concreto', 1, 0, False, 1);"; done

for i in {102..702..100}; do echo "INSERT INTO apartment(k_apartment, q_air_humidity, q_ambient_air_humidity, s_apartment_material, q_number_of_bedrooms, q_number_of_occupants, b_is_habitable, k_building) VALUES ($i, 0, 0, 'Concreto', 1, 0, False, 1);"; done

for i in {103..703..100}; do echo "INSERT INTO apartment(k_apartment, q_air_humidity, q_ambient_air_humidity, s_apartment_material, q_number_of_bedrooms, q_number_of_occupants, b_is_habitable, k_building) VALUES ($i, 0, 0, 'Concreto', 2, 0, False, 1);"; done

for i in {104..704..100}; do echo "INSERT INTO apartment(k_apartment, q_air_humidity, q_ambient_air_humidity, s_apartment_material, q_number_of_bedrooms, q_number_of_occupants, b_is_habitable, k_building) VALUES ($i, 0, 0, 'Concreto', 2, 0, False, 1);"; done

for i in {105..705..100}; do echo "INSERT INTO apartment(k_apartment, q_air_humidity, q_ambient_air_humidity, s_apartment_material, q_number_of_bedrooms, q_number_of_occupants, b_is_habitable, k_building) VALUES ($i, 0, 0, 'Concreto', 3, 0, False, 1);"; done


#Insertar Vecinos
while read apt1 apt2; do echo -e "INSERT INTO neighbor (k_apartment1, k_apartment2) VALUES (${apt1} ${apt2});" ; done < neighbors.txt



# Para la Tabla person
names=("Jhonatan" "Sofia" "Catalina" "Hanna" "Sebastian" "Sergio" "Santiago" "Maria" "Carlos" "Ana" "Luis" "Fernando" "Laura" "Felipe" "David" "Daniela" "Emmanuel" "Juan")

surnames=("Moreno" "Garcia" "Rodriguez" "Gonzalez" "Perez" "Hernandez" "Sanchez" "Diaz" "Jimenez" "Alvarez")

declare -a APARTMENTS=(101 102 103 104 105 201 202 203 204 205 301 302 303 304 305 401 402 403 404 405 501 502 503 504 505 601 602 603 604 605 701 702 703 704 705)

# Generate random data and insert into person table
for i in {1..30}
do
  # Generate random values
  k_person=$((RANDOM % 1000000000 + 100000000))
  s_name=${names[RANDOM % ${#names[@]} ]}
  s_last_name=${surnames[RANDOM % ${#surnames[@]} ]}
  s_clothing_type='Desnudo'
  k_apartment=${APARTMENTS[$((RANDOM%${#APARTMENTS[@]}))]}

  # Insert data into person table
  echo "INSERT INTO person (k_person, s_name, s_last_name, s_clothing_type, k_apartment) VALUES (${k_person}, '${s_name}', '${s_last_name}', '${s_clothing_type}', ${k_apartment});"
done

