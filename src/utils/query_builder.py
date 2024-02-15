MASTER_LEDGER_VIEW = """
        WITH cashledger_cte AS (
        SELECT 
            transaction_id, 
            date, 
            amount, 
            transaction_type, 
            account, 
            budget_id, 
            purpose_id, 
            fiscal_id, 
            details 
        FROM 
            apps_core_cashledger
        ), 
        bankledger_cte AS (
        SELECT 
            transaction_id, 
            date, 
            amount, 
            transaction_type, 
            'wells' AS account, 
            budget_id, 
            purpose_id, 
            fiscal_id, 
            details 
        FROM 
            apps_core_bankledger
        ), 
        venmoledger_cte AS (
        SELECT 
            transaction_id, 
            date, 
            net_amount AS amount, 
            transaction_type, 
            'venmo' AS account, 
            budget_id, 
            purpose_id, 
            fiscal_id, 
            note AS details 
        FROM 
            apps_core_venmoledger
        ), 
        combined_ledger_cte as (
        SELECT 
            * 
        FROM 
            cashledger_cte 
        UNION 
        SELECT 
            * 
        FROM 
            bankledger_cte 
        UNION 
        SELECT 
            * 
        FROM 
            venmoledger_cte
        ), 
        populate_budget_cte as (
        Select 
            transaction_id, 
            date, 
            amount, 
            transaction_type, 
            account, 
            value as budget, 
            purpose_id, 
            fiscal_id, 
            details 
        from 
            combined_ledger_cte 
            left join apps_core_transactioncategory on budget_id = id
        ), 
        populate_purpose_cte as (
        Select 
            transaction_id, 
            date, 
            amount, 
            transaction_type, 
            account, 
            budget, 
            value as purpose, 
            fiscal_id, 
            details 
        from 
            populate_budget_cte 
            left join apps_core_transactioncategory on purpose_id = id
        ), 
        populate_fiscal_term_cte as (
        Select 
            transaction_id, 
            date, 
            amount, 
            transaction_type, 
            account, 
            budget, 
            purpose, 
            semester as fiscal_term,
            fiscal_id, 
            details 
        from 
            populate_purpose_cte 
            left join apps_core_fiscalterm on fiscal_id = id
        ) 
        select 
        row_number() over () as id, 
        * 
        from 
        populate_fiscal_term_cte

    """
