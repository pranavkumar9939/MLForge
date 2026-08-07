export default function ModelSelector({
    models,
    selectedModel,
    onChange
}) {

    return (

        <div className="control-group">

            <label className="control-label">
                Model
            </label>

            <select 

                className="select-box"
                value = {selectedModel}
                // onChange = {(e)=>onChange(e.target.value)}
                onChange={(e)=>{
                    console.log("Selected:", e.target.value);
                    onChange(e.target.value);
                }}

            >

                {models.map(model => (

                    <option
                        key = {model}
                        value = {model}
                    >

                        {model}

                    </option>

                ))}

            </select>

        </div>

    );
}