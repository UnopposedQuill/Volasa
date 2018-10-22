use master
go
if exists(select * from sysdatabases where name = 'VolasaBackEnd')
begin
	create database VolasaBackEnd
end
go
use VolasaBackEnd
go

--tablas que no necesitan FK primero
create table Administrador(
	id int identity primary key,
	tipoAdmin bit not null,
	correo nvarchar(50),
	contrasenha nvarchar(8)
)

create table Vuelo(
	id int identity primary key,
	codigoAvion nvarchar(20) not null,
	cantidadAsientos int not null,
	aerolinea nvarchar(50) not null,
	fechaPartida datetime not null,
	fechaLlegada datetime not null,
	precio money not null,
	cantidadEscalas int not null
)

create table EquipajeRegistrado(
	id int identity primary key,
	descripcion nvarchar(100) not null,
	peso float not null
)

create table Cliente(
	id int identity primary key,
	nombre nvarchar(100) not null,
	numeroPasaporte nvarchar(50) not null,
	paisProcedencia nvarchar(50) not null,
	correo nvarchar(50) not null,
	contrasenha nvarchar(8) not null
)

create table EstadoVuelo(
	id int identity primary key,
	descripcion nvarchar(20) not null
)

--ahora las tablas que requieren FK's
create table ClienteXVuelo(
	id int identity primary key,
	FKEstadoVuelo int constraint FKClienteXVuelo_EstadoVuelo references EstadoVuelo(id),
	FKCliente int constraint FKClienteXVuelo_Cliente references Cliente(id),
	FKVuelo int constraint FKClienteXVuelo_Vuelo references Vuelo(id),
	FKAsiento int constraint FKClienteXVuelo_Asiento references Asiento(id),
	clase nvarchar(20) not null
)

create table ClienteXVueloXEquipajeRegistrado(
	id int identity primary key,
	FKClienteXVuelo int constraint FKClienteXVueloXEquipajeRegistrado_ClienteXVuelo references ClienteXVuelo(id),
	FKEquipajeRegistrado int constraint FKClienteXVueloXEquipajeRegistrado_EquipajeRegistrado references EquipajeRegistrado(id)
