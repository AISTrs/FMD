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

COMMITTEE_EXPENSE_DATA_QUERY = """
        with master_ledger_cte as (
        Select * from master_ledger where fiscal_id = {fiscal_id}
        ),
        budget_cte as (
        select value, budget
        from budget left join transaction_category on budget.category_id = transaction_category.id
        where fiscal_id = {fiscal_id}
        ),
        master_ledger_agg as (
        select budget as committee,
        round(SUM(CASE WHEN transaction_type = 'credit' THEN amount ELSE 0 END)::numeric,2) AS income,
        round(SUM(CASE WHEN transaction_type = 'debit' THEN amount ELSE 0 END)::numeric,2) AS expense
        from master_ledger_cte
        group by budget
        ),
        master_ledger_join_budget as (
        select committee, budget, income, expense
        from master_ledger_agg m left join budget_cte b on m.committee = b.value
        )
        select *, round((budget + income - expense)::numeric,2) as net, round(((abs(income - expense)/budget)*100)::numeric,2) as usage from master_ledger_join_budget;
        """
