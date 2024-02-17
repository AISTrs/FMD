MASTER_LEDGER_VIEW = """
        WITH cash_ledger_cte AS (
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
            cash_ledger
        ), 
        bank_ledger_cte AS (
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
            bank_ledger
        ), 
        venmo_ledger_cte AS (
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
            venmo_ledger
        ), 
        combined_ledger_cte as (
        SELECT 
            * 
        FROM 
            cash_ledger_cte 
        UNION 
        SELECT 
            * 
        FROM 
            bank_ledger_cte 
        UNION 
        SELECT 
            * 
        FROM 
            venmo_ledger_cte
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
            left join transaction_category on budget_id = id
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
            left join transaction_category on purpose_id = id
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
            left join fiscal_term on fiscal_id = id
        ) 
        select 
        row_number() over () as id, 
        * 
        from 
        populate_fiscal_term_cte
    """
