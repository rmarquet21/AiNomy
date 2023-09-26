package domain

type Definition struct {
	Name        string      `json:"name"`
	Description string      `json:"description"`
	KeyFactors  []keyFactor `json:"key_factors"`
	Category    string      `json:"category"`
	Tags        []tag       `json:"tags"`
	CreatedAt   interface{} `json:"created_at"`
	UpdatedAt   interface{} `json:"updated_at"`
}

type keyFactor struct {
	Name string `json:"name"`
}

type tag struct {
	Name  string `json:"name"`
	Color string `json:"color"`
}
