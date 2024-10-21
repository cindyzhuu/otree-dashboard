library(shiny)
library(readxl)
library(DT)

# Define UI for the Shiny app
ui <- fluidPage(
    titlePanel("Judiciaries"),
    sidebarLayout(
        sidebarPanel(
            fileInput("file1", "Choose Excel File",
                      accept = c(".xls", ".xlsx"))
        ),
        mainPanel(
            DTOutput("table")
        )
    )
)

# Define server logic to read and display the Excel data
server <- function(input, output) {
    # Load and display the Excel file
    output$table <- renderDT({
        req(input$file1)  # Make sure a file is uploaded
        df <- read_excel(input$file1$datapath)  # Read the Excel file
        datatable(df)  # Display it in a table
    })
}

# Run the application
shinyApp(ui = ui, server = server)