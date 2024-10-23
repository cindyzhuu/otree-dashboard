# Load libraries
library(shiny)
library(dplyr)
library(DT)
library(readxl)
library(ggplot2)

# Load the one-pagers CSV data
data <- read_excel("OnePager 2021 Q4.xlsx")

# Define UI categories
ui <- fluidPage(
    titlePanel("Judiciary One-Pagers"),

    # Select which court to view
    fluidRow(
        column(12, 
            selectInput(
                inputId = "selected_judiciary",
                label = "Select a Judiciary:",
                choices = unique(data$Court_Name),
                selected = NULL
            )
        )
    ),
    
    fluidRow(
        column(12, 
            h3(textOutput("judiciary_name"), style = "text-align: center;")
        )
    ),

    fluidRow(
        
        # Criminal Column (Summary and Top 3 Reasons row)
        column(6, 
            div(
               h4("Criminal Cases", style = "background-color: #006400; padding: 10px; color: white;"),
               h5("Summary of Key Court Events", style = "background-color: #9CAF88; padding: 10px; color: white;"),
               div(tableOutput("criminal_table"), style = "display: flex; justify-content: center;"),
               h5("Case Clearance Rate (CCR)", style = "background-color: #9CAF88; padding: 10px; color: white;"),
               plotOutput("ccr_criminal_graph"),
               h5("Top Three Reasons for Adjournments", style = "background-color: #9CAF88; padding: 10px; color: white;"),
               div(tableOutput("criminal_adjournments"), style = "display: flex; justify-content: center;"),
               style = "text-align: center;"
                )
               
            ),

        # Civil Column (Summary and Top 3 Reasons row)
        column(6, 
            div(
               h4("Civil Cases", style = "background-color: #006400; padding: 10px; color: white;"),
               h5("Summary of Key Court Events", style = "background-color: #9CAF88; padding: 10px; color: white;"),
               div(tableOutput("civil_table"), style = "display: flex; justify-content: center;"),
               h5("Case Clearance Rate (CCR)", style = "background-color: #9CAF88; padding: 10px; color: white;"),
               plotOutput("ccr_civil_graph"),
               h5("Top Three Reasons for Adjournments", style = "background-color: #9CAF88; padding: 10px; color: white;"),
               div(tableOutput("civil_adjournments"), style = "display: flex; justify-content: center;"),
               style = "text-align: center;"
               )
            )
        )
)

# Server logic
server <- function(input, output) {

    # Reactive expression to get data for the selected judiciary
    selected_judiciary_data <- reactive({
        req(input$selected_judiciary)
        data %>% filter(Court_Name == input$selected_judiciary)
    })
    
    # Display the name of the selected judiciary
    output$judiciary_name <- renderText({
        selected_judiciary_data()$Court_Name
    })
    
    # Criminal Cases Table (using hard-coded column names for civil cases)
    output$criminal_table <- renderTable({
        data <- selected_judiciary_data()
        data.frame(
            Variable = c("Criminal Cases Filed", "Criminal Cases Resolved", 
                         "Criminal Rulings & Judgments", "Criminal Adjournments"),
            Value = c(data$num_filed_Criminal, data$num_resolved_Criminal, 
                      data$num_rul_judg_Criminal, data$num_adj_Criminal)
        )
    }, rownames = FALSE)
    
    # Civil Cases Table (using hard-coded column names for civil cases)
    output$civil_table <- renderTable({
        data <- selected_judiciary_data()
        data.frame(
            Variable = c("Civil Cases Filed", "Civil Cases Resolved", 
                         "Civil Rulings & Judgments", "Civil Adjournments"),
            Value = c(data$num_filed_Civil, data$num_resolved_Civil, 
                      data$num_rul_judg_Civil, data$num_adj_Civil)
        )
    }, rownames = FALSE)
    
    # Criminal Adjournments Table (using hard-coded column names)
    # NUMBER AND PERCENT DATA LACKING
    output$criminal_adjournments <- renderTable({
        data <- selected_judiciary_data()
        data.frame(
            Rank = c(1,2,3),
            Reason = c(data$Adj_Criminal_Top_1_Name, data$Adj_Criminal_Top_2_Name, data$Adj_Criminal_Top_3_Name),
            Number = c(0,0,0),
            Percent = c(0,0,0)
        )
    }, rownames = FALSE)

    
    # Civil Adjournments Table (using hard-coded column names)
    # NUMBER AND PERCENT DATA LACKING
    output$civil_adjournments <- renderTable({
        data <- selected_judiciary_data()
        data.frame(
            Rank = c(1,2,3),
            Reason = c(data$Adj_Civil_Top_1_Name, data$Adj_Civil_Top_2_Name, data$Adj_Civil_Top_3_Name),
            Number = c(0,0,0),
            Percent = c(0,0,0)
        )
    }, rownames = FALSE)

    ccr_data <- data.frame(
        Period = c("M1", "M2", "M3"),
        criminal_ccr = c(data$CCR_Criminal, data$CCR_Criminal_L1, data$CCR_Criminal_L2),
        civil_ccr = c(data$CCR_Civil, data$CCR_Civil_L1, data$CCR_Civil_L2)
    )   

    # Generate dynamic CCR data for the selected judiciary
    output$ccr_criminal_graph <- renderPlot({
        ccr_data <- data.frame(
            Period = c("M1", "M2", "M3"),
            criminal_ccr = c(selected_judiciary_data()$CCR_Criminal, selected_judiciary_data()$CCR_Criminal_L1, selected_judiciary_data()$CCR_Criminal_L2)
        )
        ggplot(ccr_data, aes(x = Period, y = criminal_ccr)) +
        geom_bar(stat = "identity", fill = "darkred") +
        labs(title = "Criminal Case Clearance Rate (CCR)",
            x = "Period",
            y = "CCR (%)") +
        theme_minimal()
    })

    # Civil CCR Bar Plot
    output$ccr_civil_graph <- renderPlot({
        ccr_data <- data.frame(
            Period = c("M1", "M2", "M3"),
            civil_ccr = c(selected_judiciary_data()$CCR_Civil, selected_judiciary_data()$CCR_Civil_L1, selected_judiciary_data()$CCR_Civil_L2)
        )
        ggplot(ccr_data, aes(x = Period, y = civil_ccr)) +
        geom_bar(stat = "identity", fill = "darkblue") +
        labs(title = "Civil Case Clearance Rate (CCR)",
            x = "Period",
            y = "CCR (%)") +
        theme_minimal()
    })
}

# Run the app
shinyApp(ui = ui, server = server)