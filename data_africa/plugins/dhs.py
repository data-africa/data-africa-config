def start_year(df, **kwargs):
    svy = 'Survey' if not 'survey' in kwargs else kwargs['survey']
    df['start_year'] = df[svy].astype(str).str.slice(0, 4)
    return df

def convert_survey(df, **kwargs):
    svy = 'Survey' if not 'survey' in kwargs else kwargs['survey']
    df[svy] = df[svy].str.replace(" DHS", "")
    df['start_year'] = df[svy].str.split("-").apply(lambda x: x[0])
    df.loc[df[svy].str.contains("-"), 'year'] = df.loc[df[svy].str.contains("-"), svy].str.split("-").apply(lambda x: x[0][:2] + x[1])
    df.loc[~df[svy].str.contains("-"), 'year'] = df.start_year
    return df

def set_severity(df, **kwargs):
    df.loc[df.condition.str.contains("severely"), 'severity'] = 'severe'
    df.loc[~df.condition.str.contains("severely"), 'severity'] = 'moderate'
    return df

def set_condition(df, **kwargs):
    df.loc[df.condition.str.contains("stunted"), 'condition'] = 'stunted'
    df.loc[df.condition.str.contains("underweight"), 'condition'] = 'underweight'
    df.loc[df.condition.str.contains("wasted"), 'condition'] = 'wasted'
    return df

def set_gender(df, **kwargs):
    df.loc[df.Characteristic.str.contains("Male"), 'gender'] = 'male'
    df.loc[df.Characteristic.str.contains("Female"), 'gender'] = 'female'
    return df

def set_residence(df, **kwargs):
    df.loc[df.Characteristic.str.contains("Urban"), 'residence'] = 'urban'
    df.loc[df.Characteristic.str.contains("Rural"), 'residence'] = 'rural'
    return df

def fix_moderate_numbers_adm0(df, **kwargs):
    severe_cols = [col for col in df.columns if "severely" in col.lower()]
    for sev_col in severe_cols:
        moderate = sev_col.replace(" severely", "")
        # raise Exception(moderate, moderate in df.columns)
        df[moderate] = df[moderate] - df[sev_col]
    return df

def fix_moderate_numbers_adm1(df, **kwargs):
    moderate_cols = [col for col in df.columns if "moderate" in col.lower()]
    for moderate in moderate_cols:
        severe = moderate.replace("moderate", "severe")
        df[moderate] = df[moderate] - df[severe]
    return df
