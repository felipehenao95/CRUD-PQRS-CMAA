
let dataTableIsInitialized = false;
let dataTable

const dataTableOptions={
    columnDefs:[
        {className:"centered", targets: [0,1,2,3,4,5,6,7,8,9]},
    ],
    pageLength: 100,
    destroy: true,
    order: [[2, 'desc']],
    // columns: [
    //     { width: "50px" },     // # (índice)
    //     { width: "200px" },    // Nombre
    //     { width: "150px" },    // Fecha Llegada
    //     { width: "150px" },    // Fecha Entrega
    //     { width: "200px" },    // Radicado
    //     { width: "75px" },    // Localidad
    //     { width: "200px" },    // Barrio
    //     { width: "150px" },    // Tema
    //     { width: "50px" },     // Enviada
    //     { width: "200px" }     // Opciones
    // ],
    autoWidth: false
};

const initDataTable=async() =>{
    if (dataTableIsInitialized){
        dataTable.destroy();
    }
    await listProgrammers();

    dataTable=$('#datatable-peticionarios').dataTable(dataTableOptions);

    dataTableIsInitialized=true
};


const listProgrammers=async() =>{
    try{
        const response=await fetch(`/list_dps/`)
        const data=await response.json();

        let content=``;
        data.peticionarios.forEach((peticionario, index) => {
            content+=`
                <tr data-peticion="${peticionario.peticion}">
                    <td>${index}</td>
                    <td>${peticionario.nombre}</td>
                    <td>${peticionario.fecha_llegada}</td>
                    <td>${peticionario.fecha_entrega}</td>
                    <td>${peticionario.radicado}</td>
                    <td>${peticionario.localidad}</td>
                    <td>${peticionario.barrio}</td>
                    <td>${peticionario.tema_dp}</td>
                    <td>
                        ${peticionario.enviada && peticionario.enviada_aerocivil 
                            ? "<i class='fa-solid fa-check-circle' style='color: green;'></i>" 
                            : !peticionario.enviada && peticionario.enviada_aerocivil
                                ? "<i class='fa-solid fa-check' style='color: green;'></i>"
                                : peticionario.enviada_revision && !peticionario.enviada && !peticionario.enviada_aerocivil
                                    ? "<i class='fa-solid fa-search' style='color: purple;'></i>&nbsp;<i class='fa-solid fa-user-tie' style='color: purple;'></i>"
                                    : peticionario.enviada_preliminar && !peticionario.enviada_revision && !peticionario.enviada && !peticionario.enviada_aerocivil
                                        ? "<i class='fa-solid fa-user-clock' style='color: orange;'></i>"
                                        : "<i class='fa-solid fa-clock' style='color: black;'></i>"
                        }
                    </td>
                    <td>
                        <a href="/edit_dp/${peticionario.id}" class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil'></i></a>
                        <a href="/archivos/${peticionario.id}" class='btn btn-sm btn-success'><i class='fa-solid fa-upload'></i></a>
                        <a href="/proyecciones/${peticionario.id}" class='btn btn-sm btn-secondary'><i class='fa-solid fa-file-text' aria-hidden="true"></i></a>
                        <button class='btn btn-sm btn-danger delete-button' data-programmer-id="${peticionario.id}"><i class='fa-solid fa-trash-can'></i></button>
                    </td>
                    
                </tr>
            `;
        });

        tableBody_peticionarios.innerHTML = content

        document.querySelectorAll('.delete-button').forEach(button => {
            button.addEventListener('click', function() {
                const programmerId = this.getAttribute('data-programmer-id');
                if (confirm("Are you sure you want to delete this user?")) {
                    window.location.href = `/delete_user/${programmerId}/`;
                }
            });
        });

    }catch (ex) {
        alert(ex);
    }
};



window.addEventListener('load', async() => {
    await initDataTable();
});