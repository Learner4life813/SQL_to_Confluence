# SQL_to_Confluence

Problem - there was a need to automatically publish data from SQL server on an Atlasssian Confluence page.

Solution - I'm generating the SQL query results as Json (supporting on SQL Server 2017 onwards) and saving it via Confluence API as an attachment on a confluence page. 
Using TableRows Macro on confluence, I'm rendering the contents of the attachment - JSON as a datatable on the confluence page.
